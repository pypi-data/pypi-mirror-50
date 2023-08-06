"""Collection of useful decorators
"""
from ._cached_property import cached_property
from ._class_only_method import class_only_method
from ._class_property import class_property
from ._debug import debug
from ._method_decorator import method_decorator
from ._single_dispatch_method import single_dispatch_method
from ._timer import timer


__version__ = '0.1.0'
__author__ = 'Gram (@orsinium)'
__all__ = [
    'cached_property',
    'class_only_method',
    'class_property',
    'debug',
    'method_decorator',
    'single_dispatch_method',
    'timer',
]
