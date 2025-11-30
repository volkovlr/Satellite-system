import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Satellite System'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx_autodoc_typehints']
html_theme = 'sphinx_rtd_theme'