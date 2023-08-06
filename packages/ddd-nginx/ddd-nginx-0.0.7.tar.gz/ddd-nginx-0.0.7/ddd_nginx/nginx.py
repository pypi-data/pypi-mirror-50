# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
import os
from ddd_base import Aggregate
from .block import Block, TEMPLATE_DIR
from .server import Server
from .upstream import Upstream
from .map import Map
from .location import Location
from .exception import NginxError
from .file_manager import make_dir, create_file, copy_file


class Nginx(Aggregate, Block):

    def __init__(self, host):
        super().__init__()
        self._namespace = None
        self.host = host
        self.maps = []
        self.upstreams = []
        self.locations = []
        self.servers = []

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value + '.' + self.host

    def _dump_map(self, directory):
        for idx, the_map in enumerate(self.maps):
            a_map = the_map.dump("map.conf.jinja2", {
                "key_name": the_map.definition.key,
                "value_name": the_map.definition.value,
                "key_pairs": the_map.key_pairs
            })
            create_file(os.path.join(directory, str(idx) + "_map.conf"), a_map)

    def _dump_upstream(self, directory):
        for the_upstream in self.upstreams:
            a_upstream = the_upstream.dump("upstream.conf.jinja2", {
                "name": the_upstream.name,
                "servers": the_upstream.servers,
            })
            create_file(os.path.join(directory, the_upstream.name + "_upstream.conf"), a_upstream)

    def _dump_location(self, directory):
        location_dir = os.path.join(directory, "locations_conf.d")
        make_dir(location_dir)
        for idx, the_location in enumerate(self.locations):
            a_location = the_location.dump("location.jinja2.conf", {
                "name": the_location.name,
                "proxy": the_location.proxy,
                "variables": the_location.sets,
                "scope": the_location.scope
            })
            create_file(os.path.join(location_dir, str(idx) + "_location.conf"), a_location)

    def _dump_server(self, directory):
        for idx, the_server in enumerate(self.servers):
            a_server = the_server.dump("server.conf.jinja2", {
                "name": the_server.name,
                "variables": the_server.sets,
            })
            create_file(os.path.join(directory, str(idx) + "_server.conf"), a_server)

    def _dump_nginx(self, directory):
        a_nginx = self.dump("nginx.conf.jinja2", {
            "namespace": self.namespace,
        })
        create_file(os.path.join(directory, "root.conf"), a_nginx)

    def dumps(self, directory):
        make_dir(directory)
        self._dump_map(directory)
        self._dump_upstream(directory)
        self._dump_location(directory)
        self._dump_server(directory)
        self._dump_nginx(directory)
        copy_file(
            os.path.join(TEMPLATE_DIR, "error_page.conf"),
            os.path.join(directory, "error_page.conf"))

    def append(self, block):
        if isinstance(block, Server):
            self.servers.append(block)
        elif isinstance(block, Map):
            self.maps.append(block)
        elif isinstance(block, Upstream):
            self.upstreams.append(block)
        elif isinstance(block, Location):
            self.locations.append(block)
        else:
            raise NginxError()
