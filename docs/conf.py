import os
import sys

sys.path.insert(0, os.path.abspath('../mr_h4shtag'))

project = 'mr_h4shtag'
copyright = '2025, mr_h4shtag Team'
author = 'mr_h4shtag Team'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']