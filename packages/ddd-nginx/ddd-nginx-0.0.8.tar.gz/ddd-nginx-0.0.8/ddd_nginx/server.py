# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
from ddd_base import Entity
from .block import Block


class Server(Entity, Block):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def append(self):
        pass
