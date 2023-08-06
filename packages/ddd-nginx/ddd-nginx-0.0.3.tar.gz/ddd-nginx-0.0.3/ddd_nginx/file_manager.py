# -*- coding: utf-8 -*-
"""Domain Driven Design framework."""
import os
import shutil


def remove_dir(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def make_dir(directory):
    remove_dir(directory)
    os.makedirs(directory)


def create_file(file_path, content):
    with open(file_path, "w") as text_file:
        text_file.write(content)
