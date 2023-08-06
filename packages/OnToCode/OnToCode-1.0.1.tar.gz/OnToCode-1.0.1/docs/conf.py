project   = 'OnToCode'
author    = 'Philipp Matthias Schäfer'
copyright = '2018-2019, Deutsches Zentrum für Luft- und Raumfahrt e.V.'
version   = '1.0.1'
release   = '1.0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

master_doc = 'index'

html_theme = 'classic'
html_sidebars = {
    '**': ['globaltoc.html', 'searchbox.html'],
}
