from __future__ import absolute_import

from .base import Base


class PriorityQueue(Base):
    """Priority queue
    
    The lower the score, the higher the priority.
    Usage:
        pq = PriorityQueue("hello-pq")
        pq.push({"google": 100, "alibaba": 101})
        pq.pop()
    
    """
    def __len__(self):
        return self.connect().zcard(self._key)
    
    def push(self, members_with_core):
        """Push member(s) into queue
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            int: length of the queue

        """
        script = self.load_script('priority_queue_push')
        return self._run_lua_script(script, [self._key], self._make_members(members_with_core))
    
    def push_ne(self, members_with_core):
        """Push member(s) into queue only if the queue ``not already exists``
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            bool/int: False if the queue already exist else length of the queue

        """
        script = self.load_script('priority_queue_push_ne')
        rt = self._run_lua_script(script, [self._key], self._make_members(members_with_core))
        return False if rt == 'err_ae' else rt
    
    def push_ae(self, members_with_core):
        """Push member(s) into queue only if the queue ``not already exists``
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            bool/int: False if the queue already exist else length of the queue

        """
        script = self.load_script('priority_queue_push_ae')
        rt = self._run_lua_script(script, [self._key], self._make_members(members_with_core))
        return False if rt == 'err_ne' else rt
    
    def push_ni(self, member, score):
        """Push member only if it's not already inside the queue.
        
        Args:
            member (str):
            score (int):

        Returns:
            tuple: (int, bool): the queue length and a success indicator.
            
        """
        script = self.load_script('priority_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [score, member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs
    
    def pop(self, count=1):
        """Pop member(s)
        
        Args:
            count (int): How many members to pop. Defaults to 1.

        Returns:
            list/tuple/None: list if count > 1, else tuple(member, score)
                when queue is not empty, else None

        """
        script = self.load_script('priority_queue_pop')
        p = self._run_lua_script(script, [self._key], [count])
        r = self._make_return(p)
        return r if count > 1 else (r[0] if len(r) > 0 else None)
    
    def range(self, low_score='-inf', high_score='+inf'):
        """Get a range of members. Wrapper of ZRANGEBYSCORE command.
        
        Args:
            low_score (int/str):
            high_score (int/str):

        Returns:
            list:

        """
        return self.connect().zrangebyscore(self._key, low_score, high_score, None, None, True, int)

    def indexof_one(self, member):
        """Get the first index of a member
        
        Args:
            member (str): the member to search

        Returns:
            None/int: None if not found, else int

        """
        script = self.load_script('priority_queue_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexof_many(self, members):
        """Get the first index if each member
        
        Args:
            members (list): members to search

        Returns:
            dict: a dict whose key is the member and value is the member's index.
            
        """
        script = self.load_script('priority_queue_indexof')
        indexes = dict()
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    
    def _make_members(self, members):
        vl = []
        for key in members:
            vl += [members[key], key]
        return vl
    
    def _make_return(self, raw):
        r = []
        for i in range(0, len(raw)):
            if i % 2 == 0:
                r.append(
                    (raw[i], int(raw[i + 1]))
                )
        return r


class CappedPriorityQueue(PriorityQueue):
    """Priority queue with fixed capacity.
    
    Usage:
        capped_pq = CappedPriorityQueue("hello-capped-pq", 3)
    
    """
    def __init__(self, key, cap):
        """
        
        Args:
            key (str):
            cap (int):
        """
        super(CappedPriorityQueue, self).__init__(key)
        self._cap = cap
    
    def push(self, members_with_core):
        """Push member(s) into queue
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            str/int: "err_qf" if queue is already full,
                "err_qof" if queue if lacked of capacity,
                else length of the queue

        """
        script = self.load_script('capped_priority_queue_push')
        return self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
    
    def push_ne(self, members_with_core):
        """Push member(s) into queue only if the queue ``not already exists``
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            bool/int: False if the queue already exist,
                else same to `push`

        """
        script = self.load_script('capped_priority_queue_push_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
        return False if rt == 'err_ae' else rt
    
    def push_ae(self, members_with_core):
        """Push member(s) into queue only if the queue ``already exists``
        
        Args:
            members_with_core (dict): key as member and value as score(priority).

        Returns:
            bool/int: False if the queue not already exist,
                else same to `push`

        """
        script = self.load_script('capped_priority_queue_push_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
        return False if rt == 'err_ne' else rt
    
    def push_ni(self, member, score):
        """Push member into queue only if the member
        not already inside the queue.
        
        Args:
            member (str):
            score (int):

        Returns:
            str/tuple: "err_qf" if queue is already full,
                "err_qof" if queue if lacked of capacity,
                else (int: length of the queue, bool: success indicator)

        """
        script = self.load_script('capped_priority_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [self._cap, score, member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs
    

class OfCappedPriorityQueue(CappedPriorityQueue):
    """Overflow-able Priority Queue.
    
    Usage:
        of_capped_pq = OfCappedPriorityQueue("hello-of-pq", 3)
    
    """
    def push(self, members_with_core):
        """Push member(s) into queue.
        
        Args:
            members_with_core (dict):

        Returns:
            tuple: (int: length of the queue, list: members been forced out)

        """
        script = self.load_script('of_capped_priority_queue_push')
        p = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
        return p[0], self._make_return(p[1])

    def push_ne(self, members_with_core):
        """Push member(s) into queue only if the queue
        not already exist.
        
        Args:
            members_with_core (dict):

        Returns:
            bool/tuple: False if the queue already exist,
                else same to `push`.

        """
        script = self.load_script('of_capped_priority_queue_push_ne')
        p = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
        return False if p == 'err_ae' else (p[0], self._make_return(p[1]))

    def push_ae(self, members_with_core):
        """Push member(s) into queue only if the queue already exist.
        
        Args:
            members_with_core (dict):

        Returns:
            bool/tuple: False if the queue not already exist,
                else same to `push`.

        """
        script = self.load_script('of_capped_priority_queue_push_ae')
        p = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members_with_core))
        return False if p == 'err_ne' else (p[0], self._make_return(p[1]))

    def push_ni(self, member, score):
        """Push member only if it's not already inside the queue.
        
        Args:
            member (str):
            score (int):

        Returns:
            tuple: (int: the length, list: members been forced out, bool: success indicator)
            
        """
        script = self.load_script('of_capped_priority_queue_push_not_in')
        rs = self._run_lua_script(script, [self._key], [self._cap, score, member])
        return (rs[0], self._make_return(rs[1]), bool(rs[2])) if isinstance(rs, list) else rs

