#!/usr/bin/env python
from django.core.management import execute_manager
#from pydev import pydevd

#pydevd.settrace('revivan.media.mit.edu', port=51234, stdoutToServer=True, stderrToServer=True, suspend=False)
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r.\nHINT: Make sure that you have copied the settings.py.default file to settings.py.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
