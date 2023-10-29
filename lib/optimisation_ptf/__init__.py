from os.path import dirname as _dirname, basename as _basename, isfile as _isfile, join as _join
import glob as _glob
modules = _glob.glob(_join(_dirname(__file__), "*.py"))
__all__ = [_basename(f)[:-3] for f in modules if _isfile(f) and not f.endswith('__init__.py')]

from . import *
# from . import dags
#from ._read_files import Queries as show_automations
