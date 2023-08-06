# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
Template inputs aggregate :ref:`queries<queries>` and
:ref:`result processors<result-processors>`. A template input object produces
input for a template :ref:`instantiation<instantiations>` by executing its
:class:`~ontocode.query.Query` and passing it through its chain of
:ref:`result processors<result-processors>`.
"""
import abc

__all__ = ['TemplateInput']


class TemplateInput(metaclass=abc.ABCMeta):
    """Constitutes a template input consisting of a
    :class:`ontocode.query.Query` and corresponding
    :ref:`result processors<result-processors>`.

    :param ontocode.query.Query query: a query
    :param list result_processors: a list of result processors
    """

    def __init__(self, query, result_processors):
        self._query = query
        self._result_processors = result_processors

    def generate(self, world):
        """Generate template input from passed ontologies.

        :param world: an `owlready2.namespace.World` object
        :return: list of dicts or dict of lists depending on type
        """
        result = self._query.execute(world)
        for result_processor in self._result_processors:
            result = result_processor(result, world)
        return result
