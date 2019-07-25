#!/usr/bin/env python

"""
author: ares
date: 2019/5/13
desc:
"""


class Singleton(object):
    """Singleton: 在实例化的时候进行干预"""
    def __init__(self, obj):
        self.obj = obj
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self.obj not in self._instance:
            self._instance[self.obj] = self.obj(*args, **kwargs)
        return self._instance[self.obj]