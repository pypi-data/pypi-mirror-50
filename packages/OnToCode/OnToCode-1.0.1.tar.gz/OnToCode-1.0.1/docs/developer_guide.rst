Developer Guide
===============

Contributing
------------

.. include:: ../CONTRIBUTING.rst

Code Style
----------

OnToCode's code follows `PEP 8`_. This is tested by pycodestyle_, as far as
possible.

In addition, the code must pass Pylint_ as configured by our ``.pylintrc``.

Both linters are run as part of test suite, that is invoked by
``python setup.py test``.

Otherwise, the code style is only defined implicitly through the code.

.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _pycodestyle: https://pycodestyle.readthedocs.io/
.. _Pylint: https://www.pylint.org/

Architecture
------------

OnToCode is a Python 3 library project that consists of two python packages
(`ontocode` and `tests`), a directory with documentation sources (`docs`), and
a directory with test resources (`test-resources`). The `ontocode` package
contains the actual library code, while the `tests` package contains the code
for testing.

OnToCode loads ontologies with Owlready2_ and queries them with RDFLib_, it
uses Jinja2_ as a template engine, and the documentation is build with Sphinx_.

.. _Jinja2: https://pypi.org/project/Jinja2/
.. _Owlready2: https://pypi.org/project/Owlready2/
.. _RDFLib: https://pypi.org/project/rdflib/
.. _Sphinx: https://pypi.org/project/Sphinx/
