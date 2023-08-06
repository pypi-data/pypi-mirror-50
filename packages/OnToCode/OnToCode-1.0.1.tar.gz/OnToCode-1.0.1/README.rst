OnToCode (Ontology To Code) is a Python package for ontology-to-code
transformation. With OnToCode, you can instantiate templates with data queried
from ontologies.

OnToCode´s purpose is to provide software developers with a configurable,
output-format agnostic tool to generate code (and potentially other artifacts)
from ontologies. This Python package is a framework that connects a library that
loads ontologies into Python objects and can run SPARQL_\-queries against them,
with templates libraries (currently just Jinja2_) and a framework to transform
the query results into template arguments.

Guidepost
---------

This document provides information about OnToCode´s requirements, build
instructions for the documentation, a quick guide to OnToCode´s usage, as well
as copyright and licensing information.

Further information for users and developers can be found in the
documentation_, hosted on Read the Docs.

Example
~~~~~~~

The subdirectory `example` contains an elaborate example of OnToCode use.
Instructions on how to try out the example are given in the example project's
README_ file.

Requirements
------------

OnToCode was developed and tested using Python 3.6. Lower version of Python 3
might work as well. It depends on the Python packages Owlready2_ and RDFLib_,
and optionally on the Python package Jinja2_.

Building the Documentation
--------------------------

Run ``python setup.py docs`` to build the documentation. After a successful
build, the documentation can be found in ``build/sphinx/html`` with
``index.html`` as the entry page.

.. _quick-guide:

Quick Guide
-----------

This is a short introduction to OnToCode. We go through the code of a
self-contained example that can be copied into a file and run in a Python 3
environment that has OnToCode, its dependencies, and Jinja2_ installed.

We start by importing OnToCode:

.. code-block:: python

   import ontocode

To tell OnToCode which ontology to load, we create an
:class:`~ontocode.ontology.URLOntologyLocator` to load the example ontology
``http://www.w3.org/TR/2003/PR-owl-guide-20031209/food#``
from ``https://www.w3.org/TR/owl-guide/food.rdf``:

.. code-block:: python

   url = 'https://www.w3.org/TR/owl-guide/food.rdf'
   locator = ontocode.URLOntologyLocator(url)

Next, we set up a SPARQL-Query that extracts the desired data:

.. code-block:: python

   query_string = '''SELECT ?type
   WHERE {
       ?type rdfs:subClassOf
             <http://www.w3.org/TR/2003/PR-owl-guide-20031209/food##Seafood>
   }
   ORDER BY ASC(?type)'''
   query = ontocode.Query(query_string)

OnToCode runs our SPARQL_\-query against the loaded ontology. The query yields
a list of dictionaries with query variable names as keys and bound
Owlready2_ objects for the respective result rows as values. We need to convert
this result into the form that our template expects as input. This is done with
result processors:

.. code-block:: python

   processor_chain = [ontocode.ObjectNameProcessor(),
                      ontocode.list_of_dicts_to_dict_of_lists]
   template_input = ontocode.TemplateInput(query, processor_chain)

During template instantiation, the first processor is applied to the result of
the query and subsequent processors are applied, in order, to the output
of their respective predecessor.

:class:`~ontocode.result_processor.ObjectNameProcessor` converts the Owlready2_
objects in the dictionaries to their names, so we have a list of dictionaries
with variable names as keys and object names as values.

:func:`~ontocode.result_processor.list_of_dicts_to_dict_of_lists` turns our
list of dictionaries into adictionary of lists by taking the keys of the
dictionaries and assigning to each a list of all values that were previously
mapped to that key in the individual dictionaries.

Then we pass our query and the list of processors, the processor chain, into
:class:`~ontocode.template_input.TemplateInput`\´s constructor.

Next, we need a template:

.. code-block:: python

   template_string = '{% for t in type %}{{t}}{% endfor %}'
   template = ontocode.Jinja2Template.from_string(template_string)

For this example, we content ourselves with a simple
:class:`~ontocode.jinja2_template.Jinja2Template`.

Now, we have everything to instantiate our template and we do it with an
:class:`~ontocode.instantiation.Instantiation` object:

.. code-block:: python

   instantiation = ontocode.Instantiation([locator], template, [template_input])
   result = instantiation.execute()

   assert 'FishShellfish' == result[0]

Type or paste all code blocks of this section into a file, e.g.
``ontocode.py``, and run the script with ``python ontocode.py``. Make sure that
you are using Python 3 and that OnToCode as well as Jinja2_ are on the path.
When run, the script should output nothing (apart from an Owlready2_ related
warning).

As is the nature of a short introduction, we glossed over a lot of details. For
a full explanation of how to use OnToCode consult the Reference.

Copyright and License
---------------------

Copyright © 2018-2019 German Aerospace Center (DLR)

OnToCode is licensed under the Lesser General Public License Version 3 or
later. Look at the file `LICENSE`, which should be part of any OnToCode
distribution, or visit

    https://www.gnu.org/licenses/lgpl-3.0.en.html

for the full text of the license.

The example project located in the `example` subdirectory is licensed under the
General Public License Version 3 or later. See the example project's
`README.rst` file for details.

Dependencies
~~~~~~~~~~~~

OnToCode uses Sphinx for documentation generation. Version 1.8 or any later
backwards compatible version is required. Sphinx is published under a BSD
license and can be obtained from https://pypi.org/project/Sphinx/ .

OnToCode uses Owlready2 to load ontologies. Version 0.12 or any later
backwards compatible version is required. Owlready2 is published under the
LGPLv3+ and can be obtained from https://pypi.org/project/Owlready2/ .

OnToCode uses RDFLib to perform SPARQL_\-queries against ontologies. Version
4.2 or any later backwards compatible version is required. RDFLib is published
under a BSD license and can be obtained from https://pypi.org/project/rdflib/ .

OnToCode optionally uses Jinja2 as one template engine. Version 2.1 or any
later backwards compatible version is required. Jinja2 is published under a
BSD license and can be obtained from https://pypi.org/project/Jinja2/ .

.. _Jinja2: https://pypi.org/project/Jinja2/
.. _Owlready2: https://pypi.org/project/Owlready2/
.. _RDFLIB: https://pypi.org/project/rdflib/
.. _setuptools: https://pypi.org/project/setuptools/
.. _SPARQL: https://www.w3.org/TR/rdf-sparql-query/
.. _documentation: https://ontocode.readthedocs.io/en/latest/index.html
.. _README: example/README.rst
