from setuptools import setup, find_packages

setup(name='pyhomee',
      version='0.0.4',
      description='Access Homee Websocket API',
      url='http://github.com/Marmelatze/pyhomee',
      author='Florian Pfitzer',
      license='MIT',
      install_requires=['requests', 'websockets'],
      packages=find_packages(),
      zip_safe=True)
