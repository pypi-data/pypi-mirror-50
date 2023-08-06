#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicholas Earl.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from ._frontend import module_name, module_version
from ipywidgets.widgets import register, widget_serialization, Widget
from ipywidgets.widgets.trait_types import TypedTuple
from traitlets import Unicode, CaselessStrEnum, Instance, Bool


class GoldenLayout(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('IPyGLModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('IPyGLView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    selection_enabled = Bool(
        True, help="Stores a reference to the selected item.").tag(sync=True)

    # Child widgets in the container.
    # Using a tuple here to force reassignment to update the list.
    # When a proper notifying-list trait exists, use that instead.
    children = TypedTuple(trait=Instance(Widget), help="List of widget children").tag(
        sync=True, **widget_serialization)

    def __init__(self, children=(), **kwargs):
        kwargs['children'] = children
        super().__init__(**kwargs)
        self.on_displayed(GoldenLayout._fire_children_displayed)

    def _fire_children_displayed(self):
        for child in self.children:
            child._handle_displayed()
