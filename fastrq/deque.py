from __future__ import absolute_import

from .base import Base
from .loader import load


class Deque(Base):
    def __len__(self):
        return self.connect().llen(self._key)

    def push_front(self, values):
        script = load('deque_push_front')
        return self._run_lua_script(script, [self._key], self._makevalues(values))
    
    def push_back(self, values):
        script = load('deque_push_back')
        return self._run_lua_script(script, [self._key], self._makevalues(values))

    def push_front_ni(self, member):
        script = load('deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], [member])
        return [r[0], bool(r[1])]

    def push_back_ni(self, member):
        script = load('deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], [member])
        return [r[0], bool(r[1])]
    
    def pop_front(self, count=1):
        script = load('deque_pop_front')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    def pop_back(self, count=1):
        script = load('deque_pop_back')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    def range(self, start, end):
        return self.connect().lrange(self._key, start, end)

    def indexofone(self, member):
        script = load('deque_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexofmany(self, members):
        script = load('deque_indexof')
        indexes = {}
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes


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

    def push_front_ni(self, member):
        script = load('capped_deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], (self._cap, member))
        return [r[0], bool(r[1])] if isinstance(r, list) else r

    def push_back_ni(self, member):
        script = load('capped_deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], (self._cap, member))
        return [r[0], bool(r[1])] if isinstance(r, list) else r


class OfCappedDeque(CappedDeque):
    def push_front(self, values):
        script = load('of_capped_deque_push_front')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))
    
    def push_back(self, values):
        script = load('of_capped_deque_push_back')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))

    def push_front_ni(self, member):
        script = load('of_capped_deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], (self._cap, member))
        return [r[0], r[1], bool(r[2])] if isinstance(r, list) else r

    def push_back_ni(self, member):
        script = load('of_capped_deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], (self._cap, member))
        return [r[0], r[1], bool(r[2])] if isinstance(r, list) else r

