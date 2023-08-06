#!/usr/bin/env python
# coding: utf-8

from .sidepanel import SidePanel
from ._version import __version__, version_info


registry = dict()


def sidepanel(name, **kwargs):
    if name not in registry:
        if 'title' not in kwargs:
            kwargs['title'] = name
        registry[name] = SidePanel(**kwargs)
    return registry[name]

