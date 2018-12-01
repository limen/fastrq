from __future__ import absolute_import

from .base import Base
from .loader import load


class Stack(Base):
    def __len__(self):
        return self.connect().llen(self._key)
    
    def push(self, values):
        script = load('stack_push')
        return self._run_lua_script(script, (self._key,), self._makevalues(values))

    def push_ni(self, member):
        """ Push only if the member not inside the stack
        """
        script = load('stack_push_not_in')
        rs = self._run_lua_script(script, (self._key,), [member])
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs
    
    def pop(self, count=1):
        script = load('stack_pop')
        p = self._run_lua_script(script, (self._key,), (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None

    def indexofone(self, member):
        script = load('stack_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexofmany(self, members):
        script = load('stack_indexof')
        indexes = {}
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    
    
class CappedStack(Stack):
    def __init__(self, key, cap):
        super(CappedStack, self).__init__(key)
        self._cap = cap
    
    def push(self, values):
        script = load('capped_stack_push')
        return self._run_lua_script(script, (self._key,), (self._cap,) + self._makevalues(values))

    def push_ni(self, member):
        """ Push only if the member not inside the stack
        """
        script = load('capped_stack_push_not_in')
        rs = self._run_lua_script(script, (self._key,), (self._cap, member))
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs
