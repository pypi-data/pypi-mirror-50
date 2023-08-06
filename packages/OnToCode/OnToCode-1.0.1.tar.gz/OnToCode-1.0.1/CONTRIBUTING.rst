There are two ways of contributing to the development of OnToCode: reporting
issues and writing code or documentation.

If you find a bug or are missing a feature, open an issue in OnToCode's
`issue tracker`_. But before doing so, please search the tracker. Your issue
might have been addressed in the past.

If you want to contribute a patch, create a merge request on `DW's GitLab`_ to
the ``development`` branch. A patch will only be merged, if all tests pass.
Run ``python setup.py test`` to run the tests. The command will run two
linters (Pylint and pycodestyle), integration tests (pytest), and a coverage
check (Coverage.py).

You can find more information in the Developer Guide.

.. _`DW's GitLab`: https://gitlab.com/dlr-dw/ontocode/library
.. _`issue tracker`: https://gitlab.com/dlr-dw/ontocode/library/issues
