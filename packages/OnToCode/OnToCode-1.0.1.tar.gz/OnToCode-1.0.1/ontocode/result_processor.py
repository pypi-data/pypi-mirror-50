# Copyright, 2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.
# Licensed under LGPLv3+, see LICENSE for details.
"""
Result processors convert the output of :ref:`queries<queries>`, a list of
dictionaries with variable names as keys and Owlready2_ objects as values, into
the form expected by :ref:`templates<templates>`.

A template :ref:`instantiation<instantiations>` is given a list of result
processors, a result processor chain. The first element of that chain is
applied to the result of the template :ref:`instantiation<instantiations>`\\´s
query result and subsequent elements of the chain are then applied to the
output of their predecessor.

A result processor is a callable_ with two parameters, ``input_`` and
``world``. ``input_`` is the query result or the output of their predecessor,
while ``world`` is the :class:`owlready2.namespace.World` object that the query
was run against.

It is the responsibility of the user, that a result processor chain is setup,
so that the output of a result processor meets the expectations of its
successor or, for the final result processor, of the :ref:`template<templates>`
for its input value.

Built-In Result Processors
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides three result processors for commonly required
transformation tasks and a base class for result processors of a commonly
encountered transformation scheme.

.. _callable: https://docs.python.org/3/library/functions.html#callable
.. _Owlready2: https://pypi.org/project/Owlready2/
"""
import abc

__all__ = ['AbstractMapElementsProcessor', 'list_of_dicts_to_dict_of_lists',
           'NoLabelError', 'NoNameError', 'ObjectNameProcessor',
           'ObjectLabelProcessor']


class AbstractMapElementsProcessor(metaclass=abc.ABCMeta):
    """AbstractMapElementsProcessor is an abstract base class for result
    processors that expect a list of dictionaries as their ``input_``
    parameter and, when called, apply a function,
    :func:`~ontocode.result_processor.AbstractMapElementsProcessor.process_value`,
    to every value of those dictionaries.
    """

    def __call__(self, input_, world):
        """Apply
        :func:`~ontocode.result_processor.AbstractMapElementsProcessor.process_value`
        to every value of dictionaries in ``input_``.

        :param list input_: a list of dictionaries
        :return: ``input_`` with
            :func:`~ontocode.result_processor.AbstractMapElementsProcessor.process_value`
            applied to every value
        :rtype: a list of dictionaries
        """
        return [self._process_row(row, world) for row in input_]

    def _process_row(self, row, world):
        return {key: self.process_value(row[key], world) for key in row}

    @abc.abstractmethod
    def process_value(self, value, world):
        """Returns a new value derived from ``value`` and ``world``.

        :param value: some value
        :param owlready2.namespace.World world: the world object, that is the
            source of the currently processed query result"""


class ObjectNameProcessor(AbstractMapElementsProcessor):
    """Replaces Owlready2_ objects with their names."""

    def process_value(self, value, world):
        if not hasattr(value, 'name'):
            raise NoNameError()

        return value.name


class NoNameError(ValueError):
    """Raised when ObjectNameProcessor encounters an object without name."""


class ObjectLabelProcessor(AbstractMapElementsProcessor):
    """Replaces Owlready2_ objects with their English ('en') labels."""

    def process_value(self, value, world):
        if not hasattr(value, 'label'):
            raise NoLabelError()
        labels = value.label

        if not labels.en:
            raise NoLabelError()
        return labels.en[0]


class NoLabelError(ValueError):
    """Raised when ObjectLabelProcessor encounters an object without an English
    ('en') label."""


def list_of_dicts_to_dict_of_lists(input_, _world):
    """Converts a list of dicts to a dict of lists.

    Assumes that all dicts in the list of dicts have the same set of keys.

    :param list input_: a list dictionaries
    :return: a dictionary of lists
    :rtype: dict
    """
    if not input_:
        return {}
    return {k: [d[k] for d in input_] for k in input_[0]}
