#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/6/18
"""
.. currentmodule:: docstrings
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains docstring generators.
"""

from .meta import ColumnMeta, COLUMN_META_ATTR, Usage, Requirement
import inspect
from functools import wraps
from sqlalchemy import Column
from typing import List, Tuple


def model(cls):
    # We're going to go find all the members within the class hierarchy that
    # seem to be columns with metadata.
    column_members: List[Tuple[str, Column]] = []
    # Let's go through every class in the hierarchy...
    for mro in inspect.getmro(cls):
        # ...updating our list with information about all the members.
        column_members.extend(
            [
                member for member in inspect.getmembers(mro)
                if hasattr(member[1], COLUMN_META_ATTR)
            ]
        )
    # Eliminate duplicates.
    column_members = list(set(column_members))
    column_members.sort(key=lambda i: i[0])



    #nx = [x[0] for x in column_members]
    # for nnn in nx:
    #     print(nnn)

    cm_docstrings = [to_rst(cm[0], cm[1].__meta__) for cm in column_members]
    cm_docstring = '\n'.join(cm_docstrings)


    cls.__doc__ = f'{cls.__doc__}\n{cm_docstring}' if cls.__doc__ is not None else cm_docstring

    return cls


def fmt_rst(s: str, indent: int=1, wrap: bool=True):
    return '{}{}{}'.format('\t'*indent, s, '\n' if wrap else '')



def to_rst(member_name: str, meta: ColumnMeta):
    lines = [f'**{member_name}** - *{meta.label}*']
    if meta.nena is not None:
        lines.append(fmt_rst(f'NENA: *{meta.nena}*'))

    lines.append(fmt_rst('Usage'))
    excluded = {Usage.NONE}
    vals = [v for v in Usage if v not in excluded]
    tbl_borders = [None] * len(vals)
    tbl_headers = [None] * len(vals)
    tbl_values  = [None] * len(vals)
    for i in range(0, len(vals)):
        enum_name = vals[i].name
        tbl_borders[i] = '=' * len(enum_name)
        tbl_headers[i] = enum_name
        tbl_values[i] = f'✔{" " * len(enum_name)}'
    lines.append(' '.join(tbl_borders))
    lines.append(' '.join(tbl_headers))
    lines.append(' '.join(tbl_borders))
    lines.append(' '.join(tbl_values))
    lines.append(' '.join(tbl_borders))


    # Append a blank line to separate this section from the next one.
    lines.append('')
    rst = '\n'.join(lines)
    return rst
