# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
# pylint: disable=missing-docstring
import pytest

import ontocode
from tests.constants import (DEFAULT_LOCATOR, DEFAULT_QUERY, DEFAULT_RESULT,
                             DEFAULT_TEMPLATE, NAME_PROCESSOR_CHAIN,
                             LABEL_PROCESSOR_CHAIN, ONTOLOGY_PATH)


def _test_result_processor_error(query_string,
                                 processor_chain,
                                 expected_error):
    iri = 'http://example.com/products-nolabel#'
    locator = ontocode.FileSystemOntologyLocator(ONTOLOGY_PATH, iri)

    template = ontocode.Jinja2Template.from_string('')

    query = ontocode.Query(query_string)
    input_ = ontocode.TemplateInput(query, processor_chain)

    instantiation = ontocode.Instantiation([locator], template, [input_])

    with pytest.raises(expected_error):
        instantiation.execute()


def test_no_labels():
    query_string = '''
SELECT ?category
WHERE {
    ?category rdfs:subClassOf <http://example.com/products-nolabel#Product>
}'''

    _test_result_processor_error(query_string,
                                 LABEL_PROCESSOR_CHAIN,
                                 ontocode.NoLabelError)


def test_no_labels_optional():
    query_string = '''
SELECT ?label ?class
WHERE {
    ?class rdfs:subClassOf <http://example.com/products-nolabel#Product>
}'''

    _test_result_processor_error(query_string,
                                 LABEL_PROCESSOR_CHAIN,
                                 ontocode.NoLabelError)


def test_no_name():
    query_string = '''
SELECT ?label ?class
WHERE {
    ?class rdfs:subClassOf <http://example.com/products-nolabel#Product>
}'''

    _test_result_processor_error(query_string,
                                 NAME_PROCESSOR_CHAIN,
                                 ontocode.NoNameError)


def test_label():
    input_ = ontocode.TemplateInput(DEFAULT_QUERY, LABEL_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR],
                                           DEFAULT_TEMPLATE,
                                           [input_])

    result = instantiation.execute()

    assert DEFAULT_RESULT == result[0]


def test_empty_result():
    query_string = '''
SELECT ?type
WHERE {
    ?type rdfs:subClassOf <http://example.com/products#Magnetometer>
}'''
    query = ontocode.Query(query_string)
    input_ = ontocode.TemplateInput(query, NAME_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR],
                                           DEFAULT_TEMPLATE,
                                           [input_])

    result = instantiation.execute()

    assert '' == result[0]
