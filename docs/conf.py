import os
import sys

# Ajuste os caminhos conforme sua estrutura
sys.path.insert(0, os.path.abspath('../carprice-scraper'))
#sys.path.insert(0, os.path.abspath('../carprice-processor'))
# Depois adicione o API quando tiver
# sys.path.insert(0, os.path.abspath('../carprice-api'))


# -- Project information -----------------------------------------------------

project = 'CarPrice-Project'
copyright = '2025, Klylton Gomes de Souza'
author = 'Klylton Gomes de Souza'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']