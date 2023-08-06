"""Module to listen for homee events."""
import asyncio
import collections
import json
import logging
import sched
import socket
import ssl
import threading
import time
from asyncio import CancelledError

import websockets

from pyhomee.models import Attribute, Node, Group

_LOGGER = logging.getLogger(__name__)


class SubscriptionRegistry(object):
    """Class for subscribing to homee events."""

    def __init__(self, cube, loop=None):
        """Setup websocket."""
        self.ws = None
        self.cube = cube
        self.hostname = cube.hostname
        self.connected = False
        self._nodes = {}
        self._groups = []
        self._node_callbacks = collections.defaultdict(list)
        self._callbacks = list()
        self._exiting = False
        self._event_loop_thread = None
        self._loop = loop or asyncio.get_event_loop()
        # self.ping_scheduler = sched.scheduler(time.time, time.sleep)

    async def run(self):
        token = None
        while True:
            try:
                token = await self.cube.get_token()
                break  # stop retrying
            except Exception as e:
                _LOGGER.error("Failed to get homee token, trying again later: %s", e)
                await asyncio.sleep(30)

        uri = "ws://{}:7681/connection?access_token={}".format(self.hostname, token)
        while True:
            try:
                self.connection = websockets.connect(uri, subprotocols=["v2"])
                async with self.connection as ws:
                    self.ws = ws
                    _LOGGER.info("Connected to websocket")
                    await ws.send(str("GET:all"))
                    while True:
                        try:
                            message = await ws.recv()
                        except(asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=30)
                                _LOGGER.debug('Ping OK, keeping connection alive...')
                                continue
                            except:
                                await asyncio.sleep(10)
                                break  # inner loop

                        await self.on_message(message)
            except socket.gaierror:
                _LOGGER.error("Websocket connection failed")
                continue
            except ConnectionRefusedError:
                # log something else
                _LOGGER.error("Websocket connection refused")
                continue
            except CancelledError:
                _LOGGER.error("Websocket client stopped")
                break

    def register(self, node, callback):
        """Register a callback.

        node: node to be updated by subscription
        callback: callback for notification of changes
        """
        if not node:
            _LOGGER.error("Received an invalid node: %r", node)
            return

        _LOGGER.debug("Subscribing to events for %s", node)
        self._node_callbacks[node.id].append(callback)

    def register_all(self, callback):
        """Register a callback to all received events


        callback: callback for notification of changes
        """

        _LOGGER.debug("Subscribing to all events %s")
        self._callbacks.append(callback)

    def start(self):
        """Start a thread to connect to homee websocket."""
        # self._loop.set_debug(True)
        self._loop.run_until_complete(self.run())
        self._loop.run_forever()
        self._loop.close()
        _LOGGER.info("Thread started")

    async def send_command(self, command):
        try:
            await self.ws.send(command)
        except:
            _LOGGER.info("Sending command failed, restarting")

    async def send_node_command(self, node, attribute, target_value):
        return await self.send_command(
            "PUT:nodes/{}/attributes/{}?target_value={}".format(node.id, attribute.id, target_value))

    async def play_homeegram(self, id):
        return await self.send_command("PUT:homeegrams/{}?play=1".format(id))

    def _run_event_loop(self):
        token = self.cube.get_token()
        self.ws = websocket.WebSocketApp("ws://{}:7681/connection?access_token={}".format(self.hostname, token),
                                         subprotocols=["v2"],
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    async def on_message(self, message):
        if message == 'pong':
            self.connected = True
            _LOGGER.debug("pong received")
            return
        try:
            parsed = json.loads(message)
        except Exception as e:
            _LOGGER.error("Failed to parse json: " + str(e))
            return
        if "all" in parsed:
            if "nodes" in parsed['all']:
                for node in parsed['all']['nodes']:
                    self._parse_node(node)
            if "groups" in parsed['all']:
                for group in parsed['all']['groups']:
                    self._groups.append(Group(group))

        if "node" in parsed:
            self._parse_node(parsed['node'])

        if "attribute" in parsed:
            attribute = Attribute(parsed["attribute"])
            if attribute.node_id in self._node_callbacks:
                for callback in self._node_callbacks[attribute.node_id]:
                    self._loop.create_task(callback(None, attribute))
        else:
            pass

    def _parse_node(self, parsed):
        node = Node(parsed)
        self._nodes[node.id] = node
        for callback in self._callbacks:
            self._loop.create_task(callback(node))

        if node.id in self._node_callbacks:
            for callback in self._node_callbacks[node.id]:
                self._loop.create_task(callback(node, None))

    def on_error(self, error):
        _LOGGER.error("Websocket Error %s", error)
        self.restart()

    def on_close(self):
        pass

    def on_open(self):
        _LOGGER.info("Websocket opened")
        self.connected = True
        self.ping()
