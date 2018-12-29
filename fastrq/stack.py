from __future__ import absolute_import

from .base import Base


class Stack(Base):
    """Stack
    
    Usage:
        stack = Stack("hello-stack")
        stack.push("1")
        stack.push("2")
        stack.pop()
        stack.pop(2)
    """
    def __len__(self):
        return self.connect().llen(self._key)
    
    def push(self, members):
        """Push member(s) into the stack.
        
        Args:
            members (str/list): member(s) to be pushed

        Returns:
            int: The length of the stack after push
            
        """
        script = self.load_script('stack_push')
        return self._run_lua_script(script, [self._key], self._make_members(members))
    
    def push_ne(self, values):
        """Push value(s) into the stack only if the stack not already exist
        
        Args:
            values (str/list): same to `push`

        Returns:
            bool/int: False if stack not already exist else the length of the stack
            
        """
        script = self.load_script('stack_push_ne')
        rt = self._run_lua_script(script, [self._key], self._make_members(values))
        return False if rt == 'err_ae' else rt
    
    def push_ae(self, values):
        """Push value(s) into the stack only if the stack already exists
        
        Args:
            values (str/list): same to `push`

        Returns:
            bool/int: False if stack already exists else the length of the stack
            
        """
        script = self.load_script('stack_push_ae')
        rt = self._run_lua_script(script, [self._key], self._make_members(values))
        return False if rt == 'err_ne' else rt

    def push_ni(self, member):
        """Push a member only if it not already inside the stack
        
        Args:
            member (str): member to be pushed

        Returns:
            tuple(int, bool): (The stack length, True if pushed into else False)
            
        """
        script = self.load_script('stack_push_not_in')
        rs = self._run_lua_script(script, [self._key], [member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs
    
    def pop(self, count=1):
        """Pop member(s) from the stack
        
        Args:
            count (int): how many members to pop. defaults to 1.

        Returns:
            list/str/None: list if count > 1, else str if stack not empty, else None
            
        """
        script = self.load_script('stack_pop')
        p = self._run_lua_script(script, [self._key], [count])
        if count > 1:
            return [x for x in p if x is not None]
        else:
            return p[0] if len(p) > 0 else None

    def indexof_one(self, member):
        """Get the first index of a member
        
        Args:
            member (str): the member to search

        Returns:
            None/int: None if not found, else int

        """
        script = self.load_script('stack_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexof_many(self, members):
        """Get the first index if each member
        
        Args:
            members (list): members to search

        Returns:
            dict: a dict whose key is the member and value is the member's index.
            
        """
        script = self.load_script('stack_indexof')
        indexes = dict()
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    
    
class CappedStack(Stack):
    """Stack with fixed capacity.
    
    Usage:
        capped_stack = CappedStack("hello-capped-stack", 3)
    
    """
    def __init__(self, key, cap):
        """
        Args:
            key (str): the stack's ID
            cap (int): the stack's capacity
            
        """
        super(CappedStack, self).__init__(key)
        self._cap = cap
    
    def push(self, members):
        """Push member(s) into the stack
        
        Args:
            members (str/list): same to `Stack.push`

        Returns:
            str/int: "err_qf" if the stack is already full,
                "err_qof" if the stack is lacked of capacity,
                else the stack length
                
        """
        script = self.load_script('capped_stack_push')
        return self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
    
    def push_ne(self, members):
        """Push member(s) into the stack only if the stack ``not already exist``
        
        Args:
            members (str/list): same to `Stack.push`

        Returns:
            str/bool/int: "err_qf" if the stack is already full,
                "err_qof" if the stack is lacked of capacity,
                False if the stack already exists,
                else the stack length
                
        """
        script = self.load_script('capped_stack_push_ne')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ae' else rt
    
    def push_ae(self, members):
        """Push member(s) into the stack only if the stack ``already exist``
        
        Args:
            members (str/list): same to `Stack.push`

        Returns:
            str/bool/int: "err_qf" if the stack is already full,
                "err_qof" if the stack is lacked of capacity,
                False if the stack not already exist,
                else the stack length
                
        """
        script = self.load_script('capped_stack_push_ae')
        rt = self._run_lua_script(script, [self._key], [self._cap] + self._make_members(members))
        return False if rt == 'err_ne' else rt

    def push_ni(self, member):
        """Push a member only if it is not already inside the stack
        
        Args:
            member (str): same to `Stack.push_ni`

        Returns:
            tuple(int, bool): same to `Stack.push_ni`
            
        """
        script = self.load_script('capped_stack_push_not_in')
        rs = self._run_lua_script(script, [self._key], [self._cap, member])
        return (rs[0], bool(rs[1])) if isinstance(rs, list) else rs
