# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
# pylint: disable=missing-docstring
import jinja2

import ontocode
from tests.constants import (DEFAULT_LOCATOR, DEFAULT_QUERY, DEFAULT_RESULT,
                             NAME_PROCESSOR_CHAIN)


def _test_template(template):
    input_ = ontocode.TemplateInput(DEFAULT_QUERY, NAME_PROCESSOR_CHAIN)

    instantiation = ontocode.Instantiation([DEFAULT_LOCATOR], template,
                                           [input_])

    result = instantiation.execute()

    assert DEFAULT_RESULT == result[0]


def test_template_from_file():
    template = ontocode.Jinja2Template.from_file('test-resources/template')

    _test_template(template)


def test_template_from_environment():
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader('test-resources')
    )
    template = ontocode.Jinja2Template.from_environment(environment,
                                                        'template')

    _test_template(template)
