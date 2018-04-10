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


from sphinx.util.inspect import object_description
from sphinx.ext.autodoc import SUPPRESS

class MyAttributeDocumenter(AttributeDocumenter):

    def add_content(self, more_content, no_docstring=False):
        # type: (Any, bool) -> None
        if not self._datadescriptor:
            # if it's not a data descriptor, its docstring is very probably the
            # wrong thing to display
            no_docstring = True
        ClassLevelDocumenter.add_content(self, more_content, no_docstring)

    def add_directive_header(self, sig):
        # type: (unicode) -> None
        ClassLevelDocumenter.add_directive_header(self, sig)
        sourcename = self.get_sourcename()
        print(sourcename)
        if not self.options.annotation:
            if not self._datadescriptor:
                try:
                    print(1)
                    objrepr = object_description(self.object)
                except ValueError:
                    print(2)
                    pass
                else:
                    print(3)
                    pass
                    #self.add_line(u'   :annotation: = ' + objrepr, sourcename)  # This is it!!!
        elif self.options.annotation is SUPPRESS:
            print(4)
            pass
        else:
            print(5)
            self.add_line(u'   :annotation: %s' % self.options.annotation,
                          sourcename)
