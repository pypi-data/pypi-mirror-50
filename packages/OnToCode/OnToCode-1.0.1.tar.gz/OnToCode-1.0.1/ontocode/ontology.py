# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
Ontology locators tell OnToCode where to find ontologies. OnToCode uses
Owlready2_ to load ontologies and therefore supports loading `OWL 2.0`_
ontologies in the following formats:

* NTriples
* OWL/XML
* RDF/XML

Ontologies can be loaded from the file system (see
:class:`.FileSystemOntologyLocator`) or via URL (see
:class:`.URLOntologyLocator`).

An ontology locator is created by calling the constructor of a ontology locator
class.

Ontologies are loaded by :ref:`instantiations<instantiations>` for the ontology
locators passed to their constructors. Each
:ref:`instantiation<instantiations>` loads ontologies into its own
:class:`owlready2.namespace.World` object.

.. _`OWL 2.0`: https://www.w3.org/TR/owl-overview/
.. _Owlready2: https://pypi.org/project/Owlready2/
"""
import abc
import os
import owlready2 as owl

__all__ = ['FileSystemOntologyLocator', 'URLOntologyLocator']


def _load_ontology_in_world(world, iri):
    ontology = world.get_ontology(iri)
    ontology.load()


class _OntologyLocator(metaclass=abc.ABCMeta):
    """Abstract base class for ontology locator classes."""

    @abc.abstractmethod
    def load(self, world):
        """Load ontology into world.

        Loads the ontology, whose location is described by this object, into
        world.

        :param world: an `owlready2.namespace.World` object
        """


class FileSystemOntologyLocator(_OntologyLocator):
    """Specifies an ontology location in file system.

    :param str path: path to directory containing the file that describes
        the ontology with IRI ``iri`` (Not the path to a file).
    :param str iri: IRI of the ontology
    """

    def __init__(self, path, iri):
        self.path = path
        self.iri = iri

    def load(self, world):
        absolute_path = os.path.abspath(self.path)
        owl.namespace.onto_path = [absolute_path]
        _load_ontology_in_world(world, self.iri)


class URLOntologyLocator(_OntologyLocator):
    """Specifies an ontology location on the Web.

    :param str url: URL of the ontology
    """

    def __init__(self, url):
        self.url = url

    def load(self, world):
        _load_ontology_in_world(world, self.url)
