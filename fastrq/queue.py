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

    def push_ni(self, member):
        """ Push only if the member not inside the queue
        """
        script = load('queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [member])
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs
    
    def range(self, start, end):
        return self.connect().lrange(self._key, start, end)

    def indexofone(self, member):
        script = load('queue_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexofmany(self, members):
        script = load('queue_indexof')
        indexes = {}
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    

class CappedQueue(Queue):
    def __init__(self, key, cap):
        super(CappedQueue, self).__init__(key)
        self._cap = cap
    
    def push(self, values):
        script = load('capped_queue_push')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))

    def push_ni(self, member):
        """ Push only if the member not inside the queue
        """
        script = load('capped_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], (self._cap, member))
        print('capped-queue-push-ni', rs)
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs

    
class OfCappedQueue(CappedQueue):
    def push(self, values):
        script = load('of_capped_queue_push')
        return self._run_lua_script(script, [self._key], (self._cap,) + self._makevalues(values))

    def push_ni(self, member):
        """ Push only if the member not inside the queue
        """
        script = load('of_capped_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], (self._cap, member))
        return [rs[0], rs[1], bool(rs[2])] if isinstance(rs, list) else rs
