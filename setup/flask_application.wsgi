#!/usr/bin/env python

import os, sys

HOME     = '/Users/hitz'
SITE_NAME = 'ontotest'

SITE_DIR = os.path.join(HOME, 'web', SITE_NAME, 'private', SITE_NAME)
sys.path.append(SITE_DIR)

activate_this = os.path.join(HOME, 'local', 'pyenv', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from flask_application import app as application

