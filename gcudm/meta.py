#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/4/18
"""
.. currentmodule:: meta
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains metadata objects to help with inline documentation of the
model.
"""
from enum import IntFlag
from sqlalchemy import Column
from typing import Any, NamedTuple


class Requirement(IntFlag):
    """
    This enumeration describes contracts with source data providers.
    """
    NONE = 0  #: data for the column is neither requested nor required
    REQUESTED = 1  #: data for the column is requested
    REQUIRED = 3  #: data for the column is required


class Usage(IntFlag):
    """
    This enumeration describes how data may be used.
    """
    NONE = 0  #: The data is not used.
    SEARCH = 1  #: The data is used for searching.
    DISPLAY = 2  #: The data is displayed to users.


class ColumnMeta(NamedTuple):
    """
    Metadata for table columns.
    """
    label: str  #: a human-friendly column label
    nena: str = None  #: the equivalent NENA field
    requirement: Requirement = Requirement.NONE  #: the source contract
    usage: Usage = Usage.NONE  #: describes how data is used
    guaranteed: bool = False  #: Is the column guaranteed to contain a value?
    calculated: bool = False  #: May the column's value be calculated?


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

