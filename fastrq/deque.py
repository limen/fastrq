from __future__ import absolute_import

from .queue import Queue
from .loader import load


class Deque(Queue):
    def push_front(self, values):
        script = load('deque_push_front')
        return self._run_lua_script(script, [self._key], self._makevalues(values))
    
    def push_back(self, values):
        return self.push(values)
    
    def pop_front(self, count=1):
        return self.pop(count)
    
    def pop_back(self, count=1):
        script = load('deque_pop_back')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None


class CappedDeque(Deque):
    def __init__(self, key, cap):
        super(CappedDeque, self).__init__(key)
        self._cap = cap
        
    def push_front(self, values):
        script = load('capped_deque_push_front')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))
    
    def push_back(self, values):
        script = load('capped_deque_push_back')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))


class OfCappedDeque(CappedDeque):
    def push_front(self, values):
        script = load('of_capped_deque_push_front')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))
    
    def push_back(self, values):
        script = load('of_capped_deque_push_back')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))

