# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
Shared constants for tests
"""

import ontocode

ONTOLOGY_PATH = 'test-resources'
'''str: Path to directory with ontologies for tests'''

DEFAULT_LOCATOR = ontocode.FileSystemOntologyLocator(ONTOLOGY_PATH,
                                                     'http://example.com/products#')  # noqa
DEFAULT_QUERY = ontocode.Query('''
SELECT ?type
WHERE {
    ?type rdfs:subClassOf <http://example.com/products#Product>
}
ORDER BY ?type''')
DEFAULT_TEMPLATE = ontocode.Jinja2Template.from_string('{% for t in type %}{{t}}{% endfor %}')  # noqa
DEFAULT_RESULT = 'MagnetometerMagnetorquerStartracker'

NAME_PROCESSOR_CHAIN = [ontocode.ObjectNameProcessor(),
                        ontocode.list_of_dicts_to_dict_of_lists]

LABEL_PROCESSOR_CHAIN = [ontocode.ObjectLabelProcessor(),
                         ontocode.list_of_dicts_to_dict_of_lists]
