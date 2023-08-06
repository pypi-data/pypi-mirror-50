# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
OnToCode optionally provides one implementation of
:class:`ontocode.template.Template`:
:class:`ontocode.jinja2_template.Jinja2Template`. This class provides
interoperability with the Jinja2_ template library.

Note that :class:`ontocode.jinja2_template.Jinja2Template` is only available,
when the ``jinja2`` package is on the python path.

.. _Jinja2: http://jinja.pocoo.org/
"""

try:
    import jinja2
    from ontocode.template import Template

    __all__ = ['Jinja2Template']

    class Jinja2Template(Template):
        """Template class for Jinja2_ templates."""

        def __init__(self, template):
            """Create Jinja2Template object.

            :param template: a Jinja2 template
            """
            self.template = template

        @classmethod
        def from_environment(cls, environment, name):
            """Creates a Jinja2Template object with the underlying Jinja2_
            template created from a named template in a
            :class:`jinja2.Environment`.

            :param jinja2.Environment environment: a Jinja2_ environment
            :param str name: a string designating a template in
                ``environment``
            :rtype: Jinja2Template"""
            template = environment.get_template(name)
            return cls(template)

        @classmethod
        def from_file(cls, path):
            """Creates a Jinja2Template object with the underlying Jinja2_
            template created from the constants of a file.

            :param str path: path to a file containing a Jinja2_ template
            :rtype: Jinja2Template"""
            with open(path) as template_file:
                template_string = template_file.read()
                template = jinja2.Template(template_string)
                return cls(template)

        @classmethod
        def from_string(cls, string):
            """Creates a Jinja2Template object with the underlying Jinja2_
            template created from a string.

            :param str string: Jinja2_ template as string
            :rtype: Jinja2Template"""
            template = jinja2.Template(string)
            return cls(template)

        def render(self, *args, **kwargs):
            """Passes ``*args`` and ``**kwargs`` unchanged to the underlying
            Jinja2_ template."""
            return self.template.render(*args, **kwargs)

except ImportError as error:  # pragma: no cover
    if 'jinja2' != error.name:
        raise
