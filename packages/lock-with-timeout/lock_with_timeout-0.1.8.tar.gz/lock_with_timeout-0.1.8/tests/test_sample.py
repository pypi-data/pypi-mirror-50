#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 runtarou <runtarou.com@gmail.com>
#

import logging
import os

import pytest
from add_parent_path import add_parent_path

import kanilog
import stdlogging

with add_parent_path():
    from lock_with_timeout import Lock
    pass


def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_func():
    with Lock():
        pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    kanilog.setup_logger(logfile='/tmp/%s.log' % (os.path.basename(__file__)), level=logging.DEBUG)
    stdlogging.enable()
    logging.getLogger('lock_with_timeout').setLevel(logging.WARNING)

    pytest.main([__file__, '-k test_', '-s'])
