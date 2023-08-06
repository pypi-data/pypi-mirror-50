# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
# pylint: disable=missing-docstring
import ontocode
from tests.constants import (DEFAULT_LOCATOR, DEFAULT_QUERY, DEFAULT_RESULT,
                             DEFAULT_TEMPLATE, NAME_PROCESSOR_CHAIN)


def _test_locator(locator, query, expected_result):
    input_ = ontocode.TemplateInput(query, NAME_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([locator],
                                           DEFAULT_TEMPLATE,
                                           [input_])

    result = instantiation.execute()

    assert expected_result == result[0]


def test_path_locator():
    _test_locator(DEFAULT_LOCATOR, DEFAULT_QUERY, DEFAULT_RESULT)


def test_url_locator():
    query_string = '''
SELECT ?type
WHERE {
    ?type rdfs:subClassOf
          <http://www.w3.org/TR/2003/PR-owl-guide-20031209/food##Seafood>
}
ORDER BY ?type'''
    query = ontocode.Query(query_string)

    expected_result = 'FishShellfish'

    url = 'https://www.w3.org/TR/owl-guide/food.rdf'
    locator = ontocode.URLOntologyLocator(url)

    _test_locator(locator, query, expected_result)
