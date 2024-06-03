from importlib.metadata import version
try:
    __version__ = version(__name__)
except:
    __version__ = 'unknown.dev'

import os
here = __file__
basedir = os.path.split(here)[0]
example_data = os.path.join(basedir, 'example_data')
spcc_data = os.path.join(example_data, 'SPCC_SUBSET')
