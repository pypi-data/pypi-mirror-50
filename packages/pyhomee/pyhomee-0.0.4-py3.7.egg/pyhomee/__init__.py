import hashlib
import asyncio
import websockets
import time
import json
import aiohttp
import urllib
import logging

from aiohttp import BasicAuth

from pyhomee.util import get_token
from pyhomee.models import Node, Group, Homeegram, Relationship
from pyhomee.subscribe import SubscriptionRegistry

_LOGGER = logging.getLogger(__name__)


class HomeeCube():

    def __init__(self, hostname, username, password, loop=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.token = None
        self.nodes = []
        self.groups = []
        self.relationships = []
        self.homeegrams = []
        self.session = aiohttp.ClientSession()

        #self._get_all()
        self.registry = SubscriptionRegistry(self, loop=loop)

    async def _get_token(self):
        url = "http://{}:7681/access_token".format(self.hostname)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        form = {
            "device_name": "Home Assistant 2",
            "device_hardware_id": "homeassistant",
            "device_os": 5,
            "device_type": 3,
            "device_app": 1
        }
        _LOGGER.info("STart get token")
        auth = BasicAuth(self.username, hashlib.sha512(self.password.encode('utf-8')).hexdigest())
        try:
            r = await self.session.post(url, auth=auth, data=form, headers=headers, timeout=5)
        except asyncio.TimeoutError:
            raise Exception("Unable to connect to homee")
        _LOGGER.info("Finished")
        try:
            token = (await r.text()).split("&")[0].split("=")[1]
            _LOGGER.info(token)
        except:
            raise Exception("Authenticationfailed")
        return token

    async def get_token(self):
        if self.token is not None:
            return self.token
        self.token = await self._get_token()
        return self.token

    def get_nodes(self):
        return self.nodes

    def get_groups(self):
        return self.groups

    def get_relationships(self):
        return self.relationships

    def get_homeegrams(self):
        return self.homeegrams

    def get_group_by_name(self, name):
        for group in self.groups:
            if group.name == name:
                return group
        return None

    def get_group_node_ids(self, group_id):
        nodes = []
        for rel in self.relationships:
            if rel.group_id == group_id and rel.node_id != 0:
                nodes.append(rel.node_id)
        return nodes

    def register(self, node, callback):
        self.registry.register(node, callback)

    def register_all(self, callback):
        self.registry.register_all(callback)

    async def send_node_command(self, node, attribute, target_value):
        await self.registry.send_node_command(node, attribute, target_value)

    async def play_homeegram(self, id):
        await self.registry.play_homeegram(id)

    def stop(self):
        self.registry.stop()

    def run(self):
        return self.registry.run()
