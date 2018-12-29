from __future__ import absolute_import

from .base import Base


class Deque(Base):
    """Deque
    
    Usage:
        dq = Deque("hello-deque")
        dq.push_front("1")
        dq.push_back("2")
        dq.pop_front()
        dq.pop_back()
    
    """
    def __len__(self):
        return self.connect().llen(self._key)

    def push_front(self, members):
        """Push member(s) from the front end
        
        Args:
            members (str/list):

        Returns:
            int: The queue length
            
        """
        script = self.load_script('deque_push_front')
        return self._run_lua_script(script, [self._key], self._make_members(members))
    
    def push_back(self, members):
        """Push member(s) from the back end
        
        Args:
            members (str/list):

        Returns:
            int: The queue length
            
        """
        script = self.load_script('deque_push_back')
        return self._run_lua_script(script, [self._key], self._make_members(members))

    def push_front_ne(self, members):
        """Push member(s) from the front end only if the queue
        not already exists.
        
        Args:
            members (str/list):

        Returns:
            int/bool: False if the queue already exist else the queue length
            
        """
        script = self.load_script('deque_push_front_ne')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ae' else rt
    
    def push_back_ne(self, members):
        """Push member(s) from the back end only if the queue
        not already exists.
        
        Args:
            members (str/list):

        Returns:
            int/bool: False if the queue already exist else the queue length
            
        """
        script = self.load_script('deque_push_back_ne')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ae' else rt

    def push_front_ae(self, members):
        """Push member(s) from the front end only if the queue already exists.
        
        Args:
            members (str/list):

        Returns:
            int/bool: False if the queue not already exist else the queue length
            
        """
        script = self.load_script('deque_push_front_ae')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ne' else rt
    
    def push_back_ae(self, members):
        """Push member(s) from the back end only if the queue already exists.
        
        Args:
            members (str/list):

        Returns:
            int/bool: False if the queue not already exist else the queue length
            
        """
        script = self.load_script('deque_push_back_ae')
        rt = self._run_lua_script(script, [self._key], self._make_members(members))
        return False if rt == 'err_ne' else rt

    def push_front_ni(self, member):
        """Push from front end only if the member not already inside the queue
        
        Args:
            member (str): the member to push

        Returns:
            tuple: (int, bool), the queue length, True if pushed into else False
            
        """
        script = self.load_script('deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], [member])
        return r[0], bool(r[1])

    def push_back_ni(self, member):
        """Push from back end only if the member not already inside the queue
        
        Args:
            member (str): the member to push

        Returns:
            tuple: (int, bool), the queue length, True if pushed into else False
            
        """
        script = self.load_script('deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], [member])
        return r[0], bool(r[1])
    
    def pop_front(self, count=1):
        """Pop member(s) from the front end
        
        Args:
            count (int): How many members to pop. Defaults to 1.

        Returns:
            list/str/None: list if count > 1, else str if queue is not empty, else None
            
        """
        script = self.load_script('deque_pop_front')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    def pop_back(self, count=1):
        """Pop member(s) from the back end
        
        Args:
            count (int): How many members to pop. Defaults to 1.

        Returns:
            list/str/None: list if count > 1, else str if queue is not empty, else None
            
        """
        script = self.load_script('deque_pop_back')
        p = self._run_lua_script(script, [self._key], (count,))
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None
    
    def range(self, start, end):
        """Get a range of members. Wrapper of LRANGE command
        
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
        script = self.load_script('deque_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexof_many(self, members):
        """Get the first index if each member
        
        Args:
            members (list): members to search

        Returns:
            dict: a dict whose key is the member and value is the member's index.
            
        """
        script = self.load_script('deque_indexof')
        indexes = {}
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes


class CappedDeque(Deque):
    """Deque with fixed capacity
    
    Usage:
        capped_dq = CappedDeque("hello-cdq", 3)
        
    """
    def __init__(self, key, cap):
        """
        
        Args:
            key (str): queue ID
            cap (int): capacity
        """
        super(CappedDeque, self).__init__(key)
        self._cap = cap
        
    def push_front(self, members):
        """Push member(s) from the front end
        
        Args:
            members (str/list):

        Returns:
            str/int: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else the queue length
            
        """
        script = self.load_script('capped_deque_push_front')
        return self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
    
    def push_back(self, members):
        """Push member(s) from the back end
        
        Args:
            members (str/list):

        Returns:
            str/int: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else the queue length
            
        """
        script = self.load_script('capped_deque_push_back')
        return self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        
    def push_front_ne(self, members):
        """Push member(s) from the front end only if the queue
        not already exists.
        
        Args:
            members (str/list):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_front_ne`
            
        """
        script = self.load_script('capped_deque_push_front_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else rt
    
    def push_back_ne(self, members):
        """Push member(s) from the back end only if the queue
        not already exists.
        
        Args:
            members (str/list):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_back_ne`
            
        """
        script = self.load_script('capped_deque_push_back_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else rt
        
    def push_front_ae(self, members):
        """Push member(s) from the front end only if the queue already exists.
        
        Args:
            members (str/list):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_front_ae`
            
        """
        script = self.load_script('capped_deque_push_front_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else rt
    
    def push_back_ae(self, members):
        """Push member(s) from the back end only if the queue already exists.
        
        Args:
            members (str/list):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_back_ae`
            
        """
        script = self.load_script('capped_deque_push_back_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else rt

    def push_front_ni(self, member):
        """Push a member from the front end only if it's
        not already inside the queue.
        
        Args:
            member (str):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_front_ni`
            
        """
        script = self.load_script('capped_deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], [self._cap, member])
        return (r[0], bool(r[1])) if isinstance(r, list) else r

    def push_back_ni(self, member):
        """Push a member from the back end only if it's
        not already inside the queue.
        
        Args:
            member (str):

        Returns:
            str/int/bool: "err_qf" if the queue is already full,
                "err_qof" is the queue is lacked of capacity,
                else same to `Deque.push_back_ni`
            
        """
        script = self.load_script('capped_deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], [self._cap, member])
        return (r[0], bool(r[1])) if isinstance(r, list) else r


class OfCappedDeque(CappedDeque):
    """Overflow-able capped deque
    
    Usage:
        of_capped_dq = OfCappedDeque("hello-of-dq", 3)
        
    """
    def push_front(self, members):
        """Push member(s) from the front end
        
        Args:
            members (str/list):

        Returns:
            tuple: (int, list), the queue length and the members been forced out
            
        """
        script = self.load_script('of_capped_deque_push_front')
        members = self._make_members(members)
        return tuple(self._run_lua_script(script, [self._key], [self._cap] + members))
    
    def push_back(self, members):
        """Push member(s) from the back end
        
        Args:
            members (str/list):

        Returns:
            tuple: (int, list), the queue length and the members been forced out
            
        """
        script = self.load_script('of_capped_deque_push_back')
        r = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return r[0], r[1]

    def push_front_ne(self, members):
        """Push member(s) into the queue from front end
        only if the queue ``not already exist``
        
        Args:
            members (str/list):

        Returns:
            bool/tuple: False if the queue already exists,
                else (int, list): queue length, members been forced out
                
        """
        script = self.load_script('of_capped_deque_push_front_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else (rt[0], rt[1])
    
    def push_back_ne(self, members):
        """Push member(s) into the queue from back end
        only if the queue ``not already exist``
        
        Args:
            members (str/list):

        Returns:
            bool/tuple: False if the queue already exists,
                else (int, list): queue length, members been forced out
                
        """
        script = self.load_script('of_capped_deque_push_back_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else (rt[0], rt[1])

    def push_front_ae(self, members):
        """Push member(s) into the queue from front end
        only if the queue ``already exist``
        
        Args:
            members (str/list):

        Returns:
            bool/tuple: False if the queue not already exists,
                else (int, list): queue length, members been forced out
                
        """
        script = self.load_script('of_capped_deque_push_front_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else (rt[0], rt[1])
    
    def push_back_ae(self, members):
        """Push member(s) into the queue from back end
        only if the queue ``already exist``
        
        Args:
            members (str/list):

        Returns:
            bool/tuple: False if the queue not already exists,
                else (int, list): queue length, members been forced out
                
        """
        script = self.load_script('of_capped_deque_push_back_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else (rt[0], rt[1])

    def push_front_ni(self, member):
        """Push member into the queue from front end
        only if the member not already inside the queue.
        
        Args:
            member (str):

        Returns:
            tuple: (int, list, bool): queue length, members been forced out
                and an indicator
                
        """
        script = self.load_script('of_capped_deque_push_front_not_in')
        r = self._run_lua_script(script, [self._key], [self._cap, member])
        return (r[0], r[1], bool(r[2])) if isinstance(r, list) else r

    def push_back_ni(self, member):
        """Push member into the queue from back end
        only if the member not already inside the queue.
        
        Args:
            member (str):

        Returns:
            tuple: (int, list, bool): queue length, members been forced out
                and an indicator
                
        """
        script = self.load_script('of_capped_deque_push_back_not_in')
        r = self._run_lua_script(script, [self._key], (self._cap, member))
        return (r[0], r[1], bool(r[2])) if isinstance(r, list) else r

