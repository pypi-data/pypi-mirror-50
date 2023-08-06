#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicholas Earl.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..widget import GoldenLayout


def test_example_creation_blank():
    w = GoldenLayout()
    assert w.value == 'Hello World'
