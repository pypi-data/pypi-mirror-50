Reference
=========

The User Guide is aimed at software developers that want to use OnToCode in
their projects.

If you are unfamiliar with OnToCode, we recommend you to go through the
:ref:`quick-guide` to get a rough overview of how it works, before you
continue reading.

OnToCode uses Owlready2_ to load and work with ontologies as well as to query
them. Classes of this library are part of OnToCode's API, so you might need
to consult its documentation as well.

The following sections document the behavior of OnToCode's classes and their
interactions. The classes are described in an order that minimizes forward
references.

.. _Owlready2: https://pypi.org/project/Owlready2/

.. _ontology-locators:

Ontology Locators
-----------------

.. automodule:: ontocode.ontology

   .. autoclass:: FileSystemOntologyLocator

   .. autoclass:: URLOntologyLocator

.. _queries:

Queries
-------

.. automodule:: ontocode.query

   .. autoclass:: Query

.. _result-processors:

Result Processors
-----------------

.. automodule:: ontocode.result_processor

   .. autoclass:: AbstractMapElementsProcessor
      :members: process_value, __call__

   .. autoclass:: ObjectNameProcessor
      :show-inheritance:

   .. autoclass:: NoNameError
      :show-inheritance:

   .. autoclass:: ObjectLabelProcessor
      :show-inheritance:

   .. autoclass:: NoLabelError
      :show-inheritance:

   .. autofunction:: list_of_dicts_to_dict_of_lists

.. _template-inputs:

Template Inputs
---------------

.. automodule:: ontocode.template_input

   .. autoclass:: TemplateInput


.. _templates:

Templates
---------

.. automodule:: ontocode.template
   :members:

Jinja2 Template
~~~~~~~~~~~~~~~

.. automodule:: ontocode.jinja2_template

   .. autoclass:: Jinja2Template
      :show-inheritance:
      :members: from_environment, from_file, from_string, render

.. _instantiations:

Instantiations
--------------

.. automodule:: ontocode.instantiation
   :members:
