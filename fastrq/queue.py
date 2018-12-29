from __future__ import absolute_import

from .base import Base


class Queue(Base):
    """Queue
    
    Usage:
        q = Queue("hello-queue")
        q.push("world")
        q.pop()
    
    """
    def __len__(self):
        return self.connect().llen(self._key)

    def push(self, members):
        """Push member(s) into the queue
        
        Args:
            members (str/list): member(s) to be pushed

        Returns:
            int: The queue length after push
            
        """
        script = self.load_script('queue_push')
        return self._run_lua_script(script, [self._key], self._make_members(members))
    
    def pop(self, count=1):
        """Pop member(s)
        
        Args:
            count (int): How many members to pop. Defaults to 1.

        Returns:
            list/str/None: list if count > 1, else str if queue is not empty, else None
            
        """
        script = self.load_script('queue_pop')
        p = self._run_lua_script(script, [self._key], [count])
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None

    def push_ni(self, member):
        """Push only if the member not already inside the queue
        
        Args:
            member (str): the member to push

        Returns:
            tuple(int, bool): the queue length, True if pushed into else False
            
        """
        script = self.load_script('queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs

    def push_ne(self, members):
        """ Push only if the queue not already exist
        
        Args:
            members (str/list): member(s) to push
            
        Returns:
            bool/int: False if the queue already exists else the queue length
            
        """
        script = self.load_script('queue_push_ne')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ae' else rt

    def push_ae(self, members):
        """ Push only if the queue not already exist
        
        Args:
            members (str/list): member(s) to push
            
        Returns:
            bool/int: False if the queue not already exists else the queue length
            
        """
        script = self.load_script('queue_push_ae')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ne' else rt
    
    def range(self, start, end):
        """Get a range of members. Wrapper of the LRANGE command.
        
        Args:
            start (int):
            end (int):

        Returns:
            list

        """
        return self.connect().lrange(self._key, start, end)

    def indexof_one(self, member):
        """Get the first index of a member
        
        Args:
            member (str): the member to search

        Returns:
            None/int: None if not found, else int

        """
        script = self.load_script('queue_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexof_many(self, members):
        """Get the first index if each member
        
        Args:
            members (list): members to search

        Returns:
            dict: a dict whose key is the member and value is the member's index.
            
        """
        script = self.load_script('queue_indexof')
        indexes = dict()
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    

class CappedQueue(Queue):
    """Queue with a fixed capacity.
    
    Usage:
        cq = CappedQueue("hello-cq", 3)
    
    """
    def __init__(self, key, cap):
        """
        Args:
            key (str): queue's ID
            cap (int): queue's capacity
        
        """
        super(CappedQueue, self).__init__(key)
        self._cap = cap
    
    def push(self, members):
        """Push member(s) into queue
        
        Args:
            members (str/list): member(s) to push

        Returns:
            str/int: "err_qf" if queue is already full,
                "err_qof" if queue is lacked of capacity
                else the queue length
                
        """
        script = self.load_script('capped_queue_push')
        return self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
    
    def push_ne(self, members):
        """Push member(s) into the queue only if the queue ``not already exist``
        
        Args:
            members (str/list): same to `Queue.push`

        Returns:
            str/bool/int: "err_qf" if the queue is already full,
                "err_qof" if the queue is lacked of capacity,
                False if the queue already exists,
                else the queue length
                
        """
        script = self.load_script('capped_queue_push_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else rt
    
    def push_ae(self, members):
        """Push member(s) into the queue only if the queue ``already exist``
        
        Args:
            members (str/list): same to `Queue.push`

        Returns:
            str/bool/int: "err_qf" if the queue is already full,
                "err_qof" if the queue is lacked of capacity,
                False if the queue not already exists,
                else the queue length
                
        """
        script = self.load_script('capped_queue_push_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else rt

    def push_ni(self, member):
        """Push a member only if it is not already inside the queue
        
        Args:
            member (str): same to `Queue.push_ni`

        Returns:
            str/tuple: "err_qf" if queue is already full,
                "err_qof" if queue is lacked of capacity,
                else the queue length and a bool that indicate push into or not
            
        """
        script = self.load_script('capped_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [self._cap, member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs

    
class OfCappedQueue(CappedQueue):
    """Overflow-able capped queue
    
    Usage:
        of_capped_queue = OfCappedQueue("hello-of-queue", 3)
    
    """
    def push(self, members):
        """Push member(s) into queue
        
        Args:
            members (str/list): same to `Queue.push`

        Returns:
            tuple: (int, list), the queue length and the members been forced out
            
        """
        script = self.load_script('of_capped_queue_push')
        members = self._make_members(members)
        r = self._run_lua_script(script, [self._key], [self._cap] + members)
        return r[0], r[1]

    def push_ne(self, members):
        """Push member(s) into the queue only if the queue ``not already exist``
        
        Args:
            members (str/list): same to `Queue.push`

        Returns:
            bool/tuple: False if the queue already exists,
                else same to `OfCappedQueue.push`
                
        """
        script = self.load_script('of_capped_queue_push_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else (rt[0], rt[1])

    def push_ae(self, members):
        """Push member(s) into the queue only if the queue ``already exist``
        
        Args:
            members (str/list): same to `Queue.push`

        Returns:
            str/tuple: False if the queue not already exists,
                else same to `OfCappedQueue.push`
                
        """
        script = self.load_script('of_capped_queue_push_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else (rt[0], rt[1])

    def push_ni(self, member):
        """Push a member only if it is not already inside the queue
        
        Args:
            member (str): same to `OfCappedQueue.push`

        Returns:
            tuple: (int, list, bool)
                queue length, members been forced out and an indicator
            
        """
        script = self.load_script('of_capped_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [self._cap, member])
        return (rs[0], rs[1], bool(rs[2])) if isinstance(rs, list) else rs
