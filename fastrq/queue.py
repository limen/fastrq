from __future__ import absolute_import

from .base import Base
from .loader import load


class Queue(Base):
    def __len__(self):
        return self.connect().llen(self._key)
    
    def push(self, values):
        script = load('queue_push')
        return self._run_lua_script(script, [self._key], self._makevalues(values))
    
    def pop(self, count=1):
        script = load('queue_pop')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    def range(self, start, end):
        return self.connect().lrange(self._key, start, end)
    

class CappedQueue(Queue):
    def __init__(self, key, cap):
        super(CappedQueue, self).__init__(key)
        self._cap = cap
    
    def push(self, values):
        script = load('capped_queue_push')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))
    

class OfCappedQueue(CappedQueue):
    def push(self, values):
        script = load('of_capped_queue_push')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))
