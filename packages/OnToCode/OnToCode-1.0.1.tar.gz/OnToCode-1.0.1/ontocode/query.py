# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
OnToCode's queries specify SPARQL_\\-queries that are run by
:ref:`instantiations<instantiations>` against
:ref:`loaded ontologies<ontology-locators>`. A query returns a list of
dictionaries with variable names as keys and Owlready2_ objects as values.

.. _SPARQL: https://www.w3.org/TR/rdf-sparql-query/
.. _Owlready2: https://pypi.org/project/Owlready2/
"""
__all__ = ['Query']


class Query():
    """Represents a SPARQL_\\-query.

    :param str query: a SPARQL_\\-query
    """

    def __init__(self, query):
        self._query = query

    def execute(self, world):
        """Execute query against world.

        Executes SPARQL_\\-query represented by this instance against ``world``
        and returns the result.

        :param owlready2.namespace.World world: an world object
        :return: a list of dictionaries with variable names as keys and
            Owlready2_ objects as values
        :rtype: list
        """
        graph = world.as_rdflib_graph()
        rdf_result = graph.query(self._query)
        result = [_process_row(row, world) for row in rdf_result]
        return result


def _process_row(row, world):
    return {key: world[str(row[key])] for key in row.labels}
