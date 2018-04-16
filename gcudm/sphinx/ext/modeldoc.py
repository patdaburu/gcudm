#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/9/18
"""
.. currentmodule:: modeldoc.py
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains a Sphinx extension that can be used to generate specialized
documentation for model classes.
"""


from ...base import ModelMixin
from ...model import IS_MODEL_CLASS
from ...meta import (
    ColumnMeta, COLUMN_META_ATTR, TABLE_META_ATTR, Requirement, Usage
)
from sphinx.ext.autodoc import (
    ClassLevelDocumenter, AttributeDocumenter, ClassDocumenter
)
from sphinx.util.docstrings import prepare_docstring
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute
from titlecase import titlecase
from typing import Any, cast, Set, Type, Union
import uuid


__version__ = '0.0.1'  #: the version of this Sphinx extension


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_autodocumenter(ModelClassDocumenter)
    app.add_autodocumenter(ColumnAttributeDocumenter)
    return {'version': __version__, 'parallel_read_safe': True}


class ModelClassDocumenter(ClassDocumenter):
    """
    This is a specialized Documenter subclass for classes.  It overrides the
    parent class' behavior with special handling for classes that represent
    ORM model tables.
    """
    def get_doc(self, encoding=None, ignore=1):
        # Get the doc as generated by the parent class.
        doc = super().get_doc(encoding=encoding, ignore=ignore)
        # We only care about classes decorated as models.
        if not(hasattr(self.object, IS_MODEL_CLASS) and
               hasattr(self.object, TABLE_META_ATTR)):
            return doc
        # Create an image that we can put in-line with the rest of the
        # docstring.
        img_sub = str(uuid.uuid4()).replace('-', '')
        lines = [[
            f".. |{img_sub}_tbl| image:: _static/images/table.svg",
            '    :width: 24px',
            '    :height: 24px',
            ''
        ]]
        geom_markup: bool = False
        # Try to add the geometry type image.
        try:
            gtype = cast(ModelMixin, self.object).geometry_type()
            gtype_file = gtype.name.lower()
            lines[0].extend([
                f".. |{img_sub}_geom| image:: _static/images/{gtype_file}.svg",
                '    :width: 24px',
                '    :height: 24px',
                ''
            ])
            # We have geometry markup!
            geom_markup = True
        except KeyError:
            print("YYYYAAAARGHHHHH!!!")  #TODO: Improve handling!

        img_line = (
            f"|{img_sub}_tbl| |{img_sub}_geom|" if geom_markup
            else f"|{img_sub}_tbl|"
        )

        # Add the table image, along with (possibly) the geometry image and
        # the title.
        lines[0].extend([
            img_line,
            self.object.__doc__ or '', '',
            f':Table Name: {self.object.__tablename__}', ''
        ])

        # If the table has a geometry...
        geom_type = self.object.geometry_type()
        if geom_type is not None:
            # ...indicate the geometry type in the document.
            lines[0].extend([
                f':Geometry Type: {titlecase(self.object.geometry_type().name)}', ''
            ])
        # Return whatever we have.
        return lines


class ColumnAttributeDocumenter(AttributeDocumenter):
    """
    This is a specialized Documenter subclass for attributes.  It overrides the
    parent class' behavior with special handling for :py:class:`Column`
    attributes.
    """
    def add_content(self, more_content, no_docstring=False):
        # type: (Any, bool) -> None
        # Remember the original no_docstring parameter.
        _no_docstring = no_docstring
        # If this attribute appears to be a Column...
        if (isinstance(self.object, Column)
                and hasattr(self.object, COLUMN_META_ATTR)):
            # ...we really want to document it.
            _no_docstring = False
        elif not self._datadescriptor:
            # if it's not a data descriptor, its docstring is very probably the
            # wrong thing to display
            _no_docstring = True

        ClassLevelDocumenter.add_content(self, more_content, _no_docstring)

    def get_doc(self, encoding=None, ignore=1):
        # type: (unicode, int) -> List[List[unicode]]
        """Decode and return lines of the docstring(s) for the object."""
        # If the current object is a Column (or InstrumentedAttribute) and
        # it appears to have metadata...
        if (isinstance(self.object, (Column, InstrumentedAttribute)) and
                hasattr(self.object, COLUMN_META_ATTR)):
            # Get the metadata from the column.
            meta = self.object.__meta__
            # Create an image that we can put in-line with the rest of the
            # docstring.
            img_sub = str(uuid.uuid4()).replace('-', '')
            lines = [
                f".. |{img_sub}| image:: _static/images/column.svg",
                '    :width: 24px',
                '    :height: 24px',
                '',
                f"|{img_sub}| **{meta.label}**", '',
                meta.description, '',
                self.doc_enum_table(enum_cls=Usage,
                                    meta=meta,
                                    excluded={Usage.NONE}), '',
                self.doc_enum_table(enum_cls=Requirement,
                                    meta=meta,
                                    excluded={Requirement.REQUIRED}), ''
            ]
            # If the meta-data indicates there is a related NENA field...
            if meta.nena is not None:
                # ...we'll include it!
                lines.extend([f':NENA: *{meta.nena}*', ''])
            # Put it all together.
            rst = '\n'.join(lines)
            # OK, ship it out!
            return[prepare_docstring(rst, 0)]  # don't ignore it!
        else:  # In all other cases, let the parent class do its thing.
            return super().get_doc(encoding=encoding, ignore=ignore)

    @staticmethod
    def doc_enum_table(enum_cls: Type[Union[Requirement, Usage]],
                       meta: ColumnMeta,
                       excluded: Set[Any]):
        """
        Create a reStructuredText table to describe integer flag enumeration
        values.

        :param enum_cls: the enumeration type
        :param meta: the column's metadata
        :param excluded: enumeration values to be excluded from the table
        :return: the reStructuredText
        """
        # Get all of the enumerated values that aren't in the exclusion
        # set.
        vals = [v for v in enum_cls if v not in excluded]
        # Let's start off with the column specification for the table.
        colspec = f"|{'|'.join(['c'] * len(vals))}|"
        lines = [
            f'.. tabularcolumns:: {colspec}', ''
        ]
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
        # Put it all together, and...
        rst = '\n'.join(lines)
        return rst  # ...that's that.
