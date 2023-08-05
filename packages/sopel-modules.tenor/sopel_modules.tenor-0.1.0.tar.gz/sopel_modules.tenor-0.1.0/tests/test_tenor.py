#!/usr/bin/env python
# coding=utf-8
from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import unittest
import unittest.mock
import pytest

from sopel_modules.tenor import tenor


def test_template_endpoint():
    endpoint = tenor.template_endpoint('test', 'api')
    expected = 'https://api.tenor.com/v1/search?q=test&key=api&limit=10'

    assert endpoint == expected


def test_get_gifs_from_json():
    j = {'results': [{'media': [{'gif': {'url': 'test_url'}}]}]}

    url = tenor.get_gifs_from_json(j)
    expected = ['test_url']

    assert url == expected
