#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/6/18
"""
.. currentmodule:: docstrings
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains docstring generators.
"""

from .meta import ColumnMeta, COLUMN_META_ATTR, Usage, Requirement
from .modes import Modes
import inspect
from sqlalchemy import Column
import sys
from titlecase import titlecase
from typing import Any, List, Set, Tuple, Type, Union


class DocstringFormatter(object):

    @staticmethod
    def simplify_docstring(s: str):
        """
        Simplify a docstring by removing leading and trailing spaces,

        :param s:
        :return:
        """
        # Make sure we're working with an actual value.
        _s = s if s is not None else ''
        # Remove leading and trailing whitespace.
        return s.strip()

    @staticmethod
    def format_line(line: str, indent: int=1, wrap: bool=True):
        """
        Format a line of reStructuredText.

        :param line: the line to format
        :param indent: the indentation level of the formatted line
        :param wrap: Should a newline be placed at the end?
        :return: the formatted line
        """
        return '{}{}{}'.format('\t' * indent, line, '\n' if wrap else '')

    @staticmethod
    def enum2rst(enum_cls: Type[Union[Requirement, Usage]],
                 meta: ColumnMeta,
                 excluded: Set[Any],
                 indent: int = 1):
            # Let's start off with the column specification for the table.
            colspec = f"|{'|'.join(['c'] * len(vals))}|"
            lines = [
                f'.. tabularcolumns:: {colspec}', ''
            ]
            # Get all of the enumerated values that aren't in the exclusion
            # set.
            vals = [v for v in enum_cls if v not in excluded]
            # We're going to be formatting fixed-width text.  Let's do so with
            # three lists...
            tbl_hborders = [''] * len(vals)  # the horizontal borders
            tbl_headers = [''] * len(vals)  # the table headers
            tbl_values = [''] * len(vals)  # the values
            # Let's look at each of the values.
            for i in range(0, len(vals)):
                # We need the name.
                enum_name = vals[i].name
                # The character width of the column is the length of the name
                # plus one (1) padding space on each side.
                colwidth = (len(enum_name) + 2)
                # Now that we know the width, the border for this index can be
                # defined.
                tbl_hborders[i] = '-' * colwidth
                # Title-case the numeration name and place it in the headers
                # list at the current index.
                tbl_headers[i] = f' {titlecase(enum_name)} '
                # The yes-or-no indicator will only take up a single character,
                # but we need to pad it to maintain the fixed width.
                xo = [' '] * colwidth
                # Leaving one space on the left, put a yes-or-no indicator in
                # the column.  (We're using ASCII characters which we'll
                # replace in a moment.  For some reason, the extended characters
                # seem to pad the list with an extra space.)
                xo[1] = (
                    u'Y' if meta.get_enum(enum_cls) & vals[i].value else u'N'
                )
                # Build the string.
                xos = ''.join(xo)
                # Update the string with visual symbols.
                xos = xos.replace('N', '✘')
                xos = xos.replace('Y', '✔')
                # That's the text for the values list at this index.
                tbl_values[i] = xos
            # Construct the table.
            hborder = f"+{'+'.join(tbl_hborders)}+"
            lines.append(hborder)
            lines.append(f"|{'|'.join(tbl_headers)}|")
            lines.append(hborder)
            lines.append(f"|{'|'.join(tbl_values)}|")
            lines.append(hborder)
            # Indent the entire table.
            lines = [fmt_rst(line, indent=indent, wrap=False) for line in lines]
            lines.append('')  # A blank line must follow the table.
            # Put it all together, and...
            rst = '\n'.join(lines)
            return rst  # ...that's that.

    def col2rst(self,
                table_name: str,
                column_name: str,
                meta: ColumnMeta) -> str:
        """
        Format a block of reStructuredText to represent a column.

        :param table_name: the name of the table to which the column belongs
        :param column_name: the name of the column
        :param meta: the column's meta data
        :return: a block of reStructuredText
        """
        # Start by creating an internal bookmark for the column.
        lines = [f'.. _ref_{table_name}_{column_name}:']
        # Create the name of the inline image used to represent the column.
        col_img_sub = f'img_{table_name}_{column_name}'
        # Add the image definition.
        lines.append(f'.. |{col_img_sub}| image:: _static/images/column.svg')
        lines.append(fmt_rst(':width: 24px', wrap=False))
        lines.append(fmt_rst(':height: 24px', wrap=False))
        lines.append('')
        # Create the heading.
        heading = f'|{col_img_sub}| **{column_name}**'
        lines.append(heading)
        lines.append('^' * len(heading))
        # Add the label.
        lines.append(fmt_rst(f'**{meta.label}** - ', wrap=False))
        # Add the description.
        lines.append(fmt_rst(self.simplify_docstring(meta.description)))
        # Add the table of Usage values.
        lines.append(
            enum_table(enum_class=Usage, meta=meta, excluded={Usage.NONE},
                       indent=1))
        # Add the table of Requirement values.
        lines.append(
            enum_table(enum_class=Requirement, meta=meta,
                       excluded={Requirement.NONE}, indent=1))

        # If the meta-data indicates there is a related NENA field...
        if meta.nena is not None:
            # ...we'll include it!
            lines.append(fmt_rst(f':NENA: *{meta.nena}*'))

        # Append a blank line to separate this section from the next one.
        lines.append('')
        # Put it all together.
        rst = '\n'.join(lines)
        # Congratulations, we have a formatted reStructuredText string.
        return rst




def model(label: str):

    def docstring(cls):

        mod = sys.modules[cls.__module__]
        # Create the RST that defines the table image.
        col_img_sub = f'tbl_{cls.__name__}'
        lines = ['']
        if mod.__doc__ is not None:
            lines.append(mod.__doc__)

        lines.append(f'.. |{col_img_sub}| image:: _static/images/table.svg')
        lines.append(fmt_rst(':width: 24px', wrap=False))
        lines.append(fmt_rst(':height: 24px', wrap=False))
        lines.append('')

        lines.append('')
        #lines.append(f'|{col_img_sub}| **{cls.__tablename__}**')

        table_header = (
            label if label is not None
            else cls.__tablename__
        )
        table_name_header = f'|{col_img_sub}| {table_header}'
        lines.append('-' * len(table_name_header))
        lines.append(table_name_header)
        lines.append('-' * len(table_name_header))

        if cls.__doc__ is not None:
            lines.append(cls.__doc__)
            lines.append('')

        #print('\n'.join(lines))

        lines.append(fmt_rst(f':Table Name: {cls.__tablename__}'))
        lines.append(fmt_rst(f':Geometry Type: {cls.geometry_type()}'))
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

        mod.__doc__ = rst
        # Return the class.
        return cls

    def modelify(cls):
        # Update the magic 'label' property on the class.
        cls.__label__ = label
        # If we're doing a documentation run...
        if Modes().sphinx:
            # ...update the docstrings.
            docstring(cls)
        # return the original class to the caller.
        return cls

    # Return the inner function.
    return modelify



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


def simple_str(s: str):
    return s  # TODO: Improve this!


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
    lines.append(fmt_rst(simple_str(meta.description)))

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
