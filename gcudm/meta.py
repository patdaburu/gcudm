#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/4/18
"""
.. currentmodule:: meta
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains metadata objects to help with inline documentation of the
model.
"""
from sqlalchemy import Column
from typing import Any, NamedTuple


class ColumnMeta(NamedTuple):
    friendly: str
    nena: str = None


def column(dtype: Any, meta: ColumnMeta, *args, **kwargs) -> Column:
    """
    Create a GeoAlchemy :py:class:`Column` annotated with metadata.

    :param dtype: the GeoAlchemy column type
    :param meta: the meta data
    :return: a GeoAlchemy :py:class:`Column`
    """
    c = Column(dtype, *args, **kwargs)
    c.__dict__['__meta__'] = meta
    return c

