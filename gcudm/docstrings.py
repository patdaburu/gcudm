#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/6/18
"""
.. currentmodule:: docstrings
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains docstring generators.
"""

from .meta import ColumnMeta, COLUMN_META_ATTR
import inspect
from functools import wraps
from sqlalchemy import Column
from typing import Set, Tuple


def model(cls):
    # We're going to go find all the members within the class hierarcy that
    # seem to be columns with metadata.
    column_members: Set[Tuple[str, Column]] = set()
    # Let's go through every class in the hierarchy...
    for mro in inspect.getmro(cls):
        # ...updating our list with information about all the members.
        column_members.update(
            [
                member for member in inspect.getmembers(mro)
                if hasattr(member[1], COLUMN_META_ATTR)
            ]
        )

    nx = [x[0] for x in column_members]
    # for nnn in nx:
    #     print(nnn)

    cm_docstrings = [to_rst(cm[0], cm[1].__meta__) for cm in column_members]
    cm_docstring = '\n'.join(cm_docstrings)


    cls.__doc__ = f'{cls.__doc__}\n{cm_docstring}' if cls.__doc__ is not None else cm_docstring

    return cls


def to_rst(member_name: str, meta: ColumnMeta):
    lines = [f'*{member_name}*']
    lines.append('\tMore info...\n')
    return '\n'.join(lines)
