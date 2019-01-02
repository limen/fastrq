""" Fastrq: Queue, Stack and Priority Queue built on Redis.

Data types:

- Queue: nothing more to say
- Capped Queue: Queue with fixed capacity.
- Overflow-able Capped Queue: Queue with fixed capacity, and is overflow-able.

- Stack: nothing more to say
- Capped Stack: Stack with fixed capacity

- Deque: nothing more to say
- Capped Deque: Deque with fixed capacity
- Overflow-able Capped Deque: Deque with fixed capacity, and is overflow-able.

- Priority Queue: nothing more to say
- Capped Priority Queue: Priority Queue with fixed capacity
- Overflow-able Priority Queue: Priority Queue with fixed capacity, and is overflow-able.

more detail, see https://github.com/limen/fastrq

"""


from __future__ import absolute_import

from . import queue, deque, stack, priorityqueue


name = 'fastrq'
__version__ = '0.2.0'


def version():
    return __version__


__all__ = [
    queue,
    deque,
    stack,
    priorityqueue,
]
