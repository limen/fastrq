from __future__ import absolute_import

from .base import Base
from .loader import load


class Stack(Base):
    def __len__(self):
        return self.connect().llen(self._key)
    
    def push(self, values):
        script = load('stack_push')
        return self._run_lua_script(script, (self._key,), self._makevalues(values))
    
    def pop(self, count=1):
        script = load('stack_pop')
        p = self._run_lua_script(script, (self._key,), (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    
class CappedStack(Stack):
    def __init__(self, key, cap):
        super(CappedStack, self).__init__(key)
        self._cap = cap
    
    def push(self, values):
        script = load('capped_stack_push')
        return self._run_lua_script(script, (self._key,), (self._cap,) + self._makevalues(values))
