#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/9/18
"""
.. currentmodule:: __init__.py
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the '__init__.py' module.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _

from sphinx.ext.autodoc import ClassLevelDocumenter

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 4/9/18
"""
.. currentmodule:: __init__.py
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the '__init__.py' module.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _

from sphinx.ext.autodoc import (
    ClassLevelDocumenter, ModuleDocumenter, ExceptionDocumenter,
    DataDocumenter, FunctionDocumenter, MethodDocumenter, AttributeDocumenter,
    InstanceAttributeDocumenter, ClassDocumenter
)
from sqlalchemy.sql.schema import Column

__version__ = '0.0.1'

def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_autodocumenter(ModuleDocumenter)
    app.add_autodocumenter(MyClassDocumenter)  # TODO: override
    app.add_autodocumenter(ExceptionDocumenter)
    app.add_autodocumenter(DataDocumenter)
    app.add_autodocumenter(FunctionDocumenter)
    app.add_autodocumenter(MethodDocumenter)
    app.add_autodocumenter(MyAttributeDocumenter)  #: TODO: override
    app.add_autodocumenter(InstanceAttributeDocumenter)

    app.add_config_value('autoclass_content', 'class', True)
    app.add_config_value('autodoc_member_order', 'alphabetic', True)
    app.add_config_value('autodoc_default_flags', [], True)
    app.add_config_value('autodoc_docstring_signature', True, True)
    app.add_config_value('autodoc_mock_imports', [], True)
    app.add_config_value('autodoc_warningiserror', True, True)
    app.add_config_value('autodoc_inherit_docstrings', True, True)
    app.add_event('autodoc-process-docstring')
    app.add_event('autodoc-process-signature')
    app.add_event('autodoc-skip-member')

    return {'version': __version__, 'parallel_read_safe': True}  # TODO: Get version elsewhere.


class MyClassDocumenter(ClassDocumenter):

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        if hasattr(member, '__is_model_cls__'):
            print(f"****{membername}")
            return True
        else:
            print(f'NOT {membername}')
            return False


from sphinx.util.inspect import object_description, getdoc
from sphinx.util.docstrings import prepare_docstring
from sphinx.ext.autodoc import SUPPRESS
from six import text_type
from sphinx.util import force_decode

class MyAttributeDocumenter(AttributeDocumenter):

    def add_content(self, more_content, no_docstring=False):
        # type: (Any, bool) -> None
        _no_docstring = no_docstring
        print(f'self.object is a(n) {type(self.object)}')
        if isinstance(self.object, Column) and hasattr(self.object, '__meta__'):  #: TODO Get the __meta__ from the property!
            print('no_docstring=False')
            _no_docstring = False
        elif not self._datadescriptor:
            # if it's not a data descriptor, its docstring is very probably the
            # wrong thing to display
            _no_docstring = True
        ClassLevelDocumenter.add_content(self, more_content, _no_docstring)

    def add_directive_header(self, sig):
        # type: (unicode) -> None
        ClassLevelDocumenter.add_directive_header(self, sig)
        sourcename = self.get_sourcename()
        print(sourcename)
        if not self.options.annotation:
            if not self._datadescriptor:
                try:
                    objrepr = object_description(self.object)
                except ValueError:
                    pass
                else:
                    self.add_line(u'   :annotation: = ' + objrepr, sourcename)  # This is it!!!
        elif self.options.annotation is SUPPRESS:
            print(4)
            pass
        else:
            print(5)
            self.add_line(u'   :annotation: %s' % self.options.annotation,
                          sourcename)


    def get_doc(self, encoding=None, ignore=1):
        # type: (unicode, int) -> List[List[unicode]]
        """Decode and return lines of the docstring(s) for the object."""
        docstring = self.get_attr(self.object, '__doc__', None)

        print(f'type is... {type(self.object)}')
        if isinstance(self.object, Column):
            print('returning the original this!')
            return [prepare_docstring('I am a column!', ignore)]

        if docstring is None and self.env.config.autodoc_inherit_docstrings:
            docstring = getdoc(self.object)
        # make sure we have Unicode docstrings, then sanitize and split
        # into lines
        if isinstance(docstring, text_type):
            return [prepare_docstring(docstring, ignore)]
        elif isinstance(docstring, str):  # this will not trigger on Py3
            return [prepare_docstring(force_decode(docstring, encoding),
                                      ignore)]
        # ... else it is something strange, let's ignore it
        return []
