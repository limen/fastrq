from __future__ import absolute_import

from . import queue, deque, stack, priorityqueue


name = 'fastrq'
__version__ = '0.1.0'

def version():
    return __version__

__all__ = [
    queue,
    deque,
    stack,
    priorityqueue,
]
