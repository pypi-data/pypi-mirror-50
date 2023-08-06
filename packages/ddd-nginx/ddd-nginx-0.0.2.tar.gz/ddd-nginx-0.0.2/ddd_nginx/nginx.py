# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from ddd_base import Aggregate
from .block import Block
from .server import Server
from .upstream import Upstream
from .map import Map
from .exception import NginxError


class Nginx(Aggregate, Block):

    def __init__(self, host):
        super().__init__()
        self._namespace = None
        self.host = host
        self.upstreams = []
        self.maps = []
        self.servers = []

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value + '.' + self.host

    def dumps(self, path):
        pass

    def append(self, block):
        if isinstance(block, Server):
            self.servers.append(block)
        elif isinstance(block, Map):
            self.maps.append(block)
        elif isinstance(block, Upstream):
            self.upstreams.append(block)
        else:
            raise NginxError()
