#!/usr/bin/env python

"""
author: ares
date: 2019/5/12
desc:
"""
import time
import inspect


def get_current_func_name():
    """get current func name"""
    return inspect.stack()[1][3]


def get_current_time():
    """get format current time"""
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
