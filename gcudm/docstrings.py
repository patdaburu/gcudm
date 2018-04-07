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
import sys
from titlecase import titlecase
from typing import Any, List, Set, Tuple, Type


def model(cls):

    # Create the RST that defines the table image.
    col_img_sub = f'tbl_{cls.__name__}'
    lines = ['']
    lines.append(f'.. |{col_img_sub}| image:: _static/images/table.svg')
    lines.append(fmt_rst(':width: 24px', wrap=False))
    lines.append(fmt_rst(':height: 24px', wrap=False))
    lines.append('')

    lines.append('')
    #lines.append(f'|{col_img_sub}| **{cls.__tablename__}**')

    table_header = (
        cls.__label__ if cls.__label__ is not None
        else cls.__tablename__
    )
    table_name_header = f'|{col_img_sub}| {table_header}'
    lines.append('-' * len(table_name_header))
    lines.append(table_name_header)
    lines.append('-' * len(table_name_header))

    #print('\n'.join(lines))

    lines.append(fmt_rst(f':Table Name: {cls.__tablename__}'))
    lines.append(fmt_rst(f':Geometry Type: {cls.get_geometry_type()}'))
    # if cls.__doc__ is not None:
    #     lines.append(cls.__doc__)

    lines.append('')

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
    # Create the RST documentation for all the column members.
    cm_docstrings = [to_rst(cm[0], cm[1].__meta__) for cm in column_members]
    cm_docstring = '\n'.join(cm_docstrings)

    # Add the collected docstrings for the tables.
    lines.append(cm_docstring)




    #cls.__doc__ = f'{cls.__doc__}\n{cm_docstring}' if cls.__doc__ is not None else cm_docstring
    rst = '\n'.join(lines)
    #cls.__doc__ = rst

    mod = sys.modules[cls.__module__]
    mod.__doc__ = rst



    return cls


def fmt_rst(s: str, indent: int=1, wrap: bool=True):
    return '{}{}{}'.format('\t'*indent, s, '\n' if wrap else '')

def enum_table(
        enum_class: Type,
        meta: ColumnMeta,
        excluded: Set[Any],
        indent: int = 1):
    lines = []
    vals = [v for v in enum_class if v not in excluded]
    colspec = f"|{'|'.join(['c'] * len(vals))}|"
    lines.append(f'.. tabularcolumns:: {colspec}')
    lines.append('')
    tbl_hborders = [''] * len(vals)
    tbl_headers = [''] * len(vals)
    tbl_values = [''] * len(vals)
    for i in range(0, len(vals)):
        enum_name = vals[i].name
        colwidth = (len(enum_name) + 2)
        tbl_hborders[i] = '-' * colwidth
        tbl_headers[i] = f' {titlecase(enum_name)} '
        xo = [' '] * colwidth
        xo[1] = u'Y' if meta.get_enum(enum_class) & vals[i].value else u'N'  # TODO: Get actual value!
        xos = ''.join(xo)
        # Update the string with visual symbols.
        xos = xos.replace('N', '✘')
        xos = xos.replace('Y', '✔')
        tbl_values[i] = xos
    # Construct the table.
    hborder = f"+{'+'.join(tbl_hborders)}+"
    lines.append(hborder)
    lines.append(f"|{'|'.join(tbl_headers)}|")
    lines.append(hborder)
    lines.append(f"|{'|'.join(tbl_values)}|")
    lines.append(hborder)

    lines = [fmt_rst(line, indent=indent, wrap=False) for line in lines]
    lines.append('')
    rst = '\n'.join(lines)
    return rst


def to_rst(member_name: str, meta: ColumnMeta):
    col_img_sub = f'column_{member_name}'
    lines = ['']
    lines.append(f'.. _ref_{member_name}:')

    lines.append(f'.. |{col_img_sub}| image:: _static/images/column.svg')
    lines.append(fmt_rst(':width: 24px', wrap=False))
    lines.append(fmt_rst(':height: 24px', wrap=False))
    lines.append('')

    # lines.append('-' * len(member_name))
    # lines.append(member_name)
    # lines.append('-' * len(member_name))

    #

    member_heading = f'|{col_img_sub}| **{member_name}**'
    lines.append(member_heading)
    lines.append('^' * len(member_heading))

    lines.append(fmt_rst(f'**{meta.label}** - ', wrap=False))
    lines.append(fmt_rst(meta.fmt_description()))

    #lines.append('')
    lines.append(enum_table(enum_class=Usage, meta=meta, excluded={Usage.NONE}, indent=1))

    lines.append(
        enum_table(enum_class=Requirement, meta=meta, excluded={Requirement.NONE}, indent=1))

    if meta.nena is not None:
        lines.append(fmt_rst(f':NENA: *{meta.nena}*'))

    # Append a blank line to separate this section from the next one.
    lines.append('')

    #lines = [fmt_rst(line, indent=1, wrap=False) for line in lines]

    rst = '\n'.join(lines)

    # print(rst)

    return rst
