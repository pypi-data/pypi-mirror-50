# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
# pylint: disable=missing-docstring
import pytest

import ontocode
from tests.constants import (DEFAULT_LOCATOR, DEFAULT_QUERY, DEFAULT_RESULT,
                             DEFAULT_TEMPLATE, NAME_PROCESSOR_CHAIN)


def _test_file_content(path, expected_content):
    with open(path) as outputfile:
        written_content = outputfile.read()
        assert expected_content == written_content


def test_execute_and_write_to_file():
    input_ = ontocode.TemplateInput(DEFAULT_QUERY, NAME_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR],
                                           DEFAULT_TEMPLATE,
                                           [input_])

    file_path = '/tmp/testoutput'

    instantiation.execute_and_write_to_file(file_path)

    _test_file_content(file_path, DEFAULT_RESULT)


def test_execute_and_write_to_file_per_row_input_not_null():
    input_ = ontocode.TemplateInput(DEFAULT_QUERY, NAME_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR],
                                           DEFAULT_TEMPLATE,
                                           [],
                                           input_)

    file_path = '/tmp/testoutput'

    with pytest.raises(ontocode.TemplateInputArgumentError):
        instantiation.execute_and_write_to_file(file_path)


def test_execute_and_write_to_files():
    template_string = '{{type}}'
    template = ontocode.Jinja2Template.from_string(template_string)

    processors = [ontocode.ObjectNameProcessor()]
    input_ = ontocode.TemplateInput(DEFAULT_QUERY, processors)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR], template, [],
                                           input_)

    def path_function(*_args, **kwargs):
        return '/tmp/' + kwargs['type']

    instantiation.execute_and_write_to_files(path_function)

    for type_ in ['Magnetometer', 'Magnetorquer', 'Startracker']:
        _test_file_content('/tmp/' + type_, type_)


def _constantly_none(_result, _world):
    pass


def _test_wrong_result(execute, input_class):

    input_ = input_class(DEFAULT_QUERY, [_constantly_none])

    template = ontocode.Jinja2Template.from_string('')

    with pytest.raises(ontocode.TemplateInputResultError):
        execute(DEFAULT_LOCATOR, template, input_)


def test_wrong_result_type_at_once():
    def execute(locator, template, input_):
        instantiation = ontocode.Instantiation([locator], template, [input_])
        instantiation.execute()

    _test_wrong_result(execute, ontocode.TemplateInput)


def test_wrong_result_type_per_row():
    def execute(locator, template, input_):
        instantiation = ontocode.Instantiation([locator], template, [], input_)
        instantiation.execute()

    _test_wrong_result(execute, ontocode.TemplateInput)
