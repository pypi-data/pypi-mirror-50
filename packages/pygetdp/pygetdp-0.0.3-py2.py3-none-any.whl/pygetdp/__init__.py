# -*- coding: utf-8 -*-
#

"""
pygetdp
==============

Python frontend for GetDP.




"""


from __future__ import print_function

from .__about__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __status__,
    __version__,
    __website__,
)
from .constraint import Constraint
from .formulation import Formulation
from .function import Function
from .functionspace import FunctionSpace
from .getdp_object import GetDPObject
from .group import Group
from .integration import Integration
from .jacobian import Jacobian
from .postoperation import PostOperation
from .postprocessing import PostProcessing
from .problem_definition import Problem
from .rendering import *
from .resolution import Resolution

# __doc__ = __description__


__all__ = ["__version__", "__author__", "__author_email__", "__website__"]

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end="")
