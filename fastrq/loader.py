_scripts = {}

_scripts['queue_push'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('rpush',KEYS[1],k)
end
return len
"""

_scripts['queue_push_not_in'] = """
local len=redis.call('llen',KEYS[1])
local iv
local i=0
while i<len and iv~=ARGV[1] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[1] then
  len=redis.call('rpush',KEYS[1],ARGV[1])
  y=1
end
return {len,y}
"""

_scripts['queue_pop'] = """
local o={}
for i=1,tonumber(ARGV[1]) do
  o[#o + 1]=redis.call('lpop',KEYS[1])
end
return o
"""

_scripts['capped_queue_push'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + #ARGV - 1 > cap then
  return 'err_qof'
end
for i,k in ipairs(ARGV) do
  if i > 1 then
    len=redis.call('rpush',KEYS[1],k)
  end
end
return len
"""

_scripts['capped_queue_push_not_in'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len>=cap then
  return 'err_qf'
elseif len+#ARGV-1>cap then
  return 'err_qof'
end
local i=0
local iv
local y=0
while i<len and iv~=ARGV[2] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
if iv~=ARGV[2] then
  len=redis.call('rpush',KEYS[1],ARGV[2])
  y=1
end
return {len,y}
"""

_scripts['of_capped_queue_push'] = """
local cap=tonumber(ARGV[1])
for i,k in ipairs(ARGV) do
  if i > 1 then
    redis.call('rpush',KEYS[1],k)
  end
end
local len=redis.call('llen',KEYS[1])
local o={}
while len > cap do
  o[#o + 1]=redis.call('lpop',KEYS[1])
  len=len - 1
end
return { len,o }
"""

_scripts['of_capped_queue_push_not_in'] = """
local cap=tonumber(ARGV[1])
local len=redis.call('llen',KEYS[1])
local i=0
local iv
while i<len and iv~=ARGV[2] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[2] then
  len=redis.call('rpush',KEYS[1],ARGV[2])
  y=1
end
local o={}
while len>cap do
  o[#o+1]=redis.call('lpop',KEYS[1])
  len=len-1
end
return {len,o,y}
"""

_scripts['deque_push_front'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('lpush',KEYS[1],k)
end
return len
"""

_scripts['deque_push_front_not_in'] = """
local len=redis.call('llen',KEYS[1])
local iv
local i=0
while i<len and iv~=ARGV[1] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[1] then
  len=redis.call('lpush',KEYS[1],ARGV[1])
  y=1
end
return {len,y}
"""

_scripts['deque_pop_back'] = """
local o={}
for i=1,tonumber(ARGV[1]) do
  o[#o + 1]=redis.call('rpop',KEYS[1])
end
return o
"""

_scripts['capped_deque_push_front'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + #ARGV - 1 > cap then
  return 'err_qof'
end
for i,k in ipairs(ARGV) do
  if i > 1 then
    len=redis.call('lpush',KEYS[1],k)
  end
end
return len
"""

_scripts['capped_deque_push_front_not_in'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + #ARGV - 1 > cap then
  return 'err_qof'
end
local iv
local i=0
local y=0
while i<len and iv~=ARGV[2] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
if iv~=ARGV[2] then
  len=redis.call('lpush',KEYS[1],ARGV[2])
  y=1
end
return {len,y}
"""

_scripts['of_capped_deque_push_front'] = """
local cap=tonumber(ARGV[1])
for i,k in ipairs(ARGV) do
  if i > 1 then
    redis.call('lpush',KEYS[1],k)
  end
end
local len=redis.call('llen',KEYS[1])
local o={}
while len > cap do
  o[#o + 1]=redis.call('rpop',KEYS[1])
  len=len - 1
end
return { len,o }
"""

_scripts['of_capped_deque_push_front_not_in'] = """
local cap=tonumber(ARGV[1])
local len=redis.call('llen',KEYS[1])
local iv
local i=0
while i<len and iv~=ARGV[2] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[2] then
  len=redis.call('lpush',KEYS[1],ARGV[2])
  y=1
end
local o={}
while len>cap do
  o[#o+1]=redis.call('rpop',KEYS[1])
  len=len-1
end
return {len,o,y}
"""

_scripts['stack_push'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('lpush',KEYS[1],k)
end
return len
"""

_scripts['stack_push_not_in'] = """
local len=redis.call('llen',KEYS[1])
local iv
local i=0
while i<len and iv~=ARGV[1] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[1] then
  len=redis.call('lpush',KEYS[1],ARGV[1])
  y=1
end
return {len,y}
"""

_scripts['stack_pop'] = """
local o={}
for i=1,tonumber(ARGV[1]) do
  o[#o + 1]=redis.call('lpop',KEYS[1])
end
return o
"""

_scripts['capped_stack_push'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + #ARGV - 1 > cap then
  return 'err_qof'
end
for i,k in ipairs(ARGV) do
  if i > 1 then
    len=redis.call('lpush',KEYS[1],k)
  end
end
return len
"""

_scripts['capped_stack_push_not_in'] = """
local len=redis.call('llen',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + #ARGV - 1 > cap then
  return 'err_qof'
end
local iv
local i=0
while i<len and iv~=ARGV[2] do
  iv=redis.call('lindex',KEYS[1],i)
  i=i+1
end
local y=0
if iv~=ARGV[2] then
  len=redis.call('lpush',KEYS[1],ARGV[2])
  y=1
end
return {len,y}
"""

_scripts['priority_queue_push'] = """
local i=1
while i < #ARGV do
  redis.call('zadd',KEYS[1],ARGV[i],ARGV[i + 1])
  i=i + 2
end
return redis.call('zcard',KEYS[1])
"""

_scripts['priority_queue_push_not_in'] = """
local len=redis.call('zcard',KEYS[1])
local y=0
local rank=redis.call('zrank',KEYS[1],ARGV[2])
if not rank then
  redis.call('zadd',KEYS[1],ARGV[1],ARGV[2])
  len=redis.call('zcard',KEYS[1])
  y=1
end
return {len,y}
"""

_scripts['priority_queue_pop'] = """
local h=redis.call('zrange',KEYS[1],0,tonumber(ARGV[1]) - 1,'WITHSCORES')
local i=1
while i < #h do
  redis.call('zrem',KEYS[1],h[i])
  i=i + 2
end
return h
"""

_scripts['capped_priority_queue_push'] = """
local len=redis.call('zcard',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + (#ARGV - 1) / 2 > cap then
  return 'err_qof'
end
local i=2
while i < #ARGV do
  redis.call('zadd',KEYS[1],ARGV[i],ARGV[i + 1])
  i=i + 2
end
return redis.call('zcard',KEYS[1])
"""

_scripts['capped_priority_queue_push_not_in'] = """
local len=redis.call('zcard',KEYS[1])
local cap=tonumber(ARGV[1])
if len >= cap then
  return 'err_qf'
elseif len + (#ARGV - 1) / 2 > cap then
  return 'err_qof'
end
local y=0
if not redis.call('zrank',KEYS[1],ARGV[3]) then
  redis.call('zadd',KEYS[1],ARGV[2],ARGV[3])
  y=1
end
return {redis.call('zcard',KEYS[1]),y}
"""

_scripts['of_capped_priority_queue_push'] = """
local cap=tonumber(ARGV[1])
local i=2
while i<#ARGV do
  redis.call('zadd',KEYS[1],ARGV[i],ARGV[i + 1])
  i=i+2
end
local c=redis.call('zcard',KEYS[1])
local o={}
if c>cap then
  o=redis.call('zrange',KEYS[1],cap - c,-1,'WITHSCORES')
  for i,m in ipairs(o) do
    if i % 2 == 1 then
      redis.call('zrem',KEYS[1],m)
      c=c-1
    end
  end
end
return {c,o}
"""

_scripts['of_capped_priority_queue_push_not_in'] = """
local cap=tonumber(ARGV[1])
local y=0
if not redis.call('zrank',KEYS[1],ARGV[3]) then
  redis.call('zadd',KEYS[1],ARGV[2],ARGV[3])
  y=1
end
local c=redis.call('zcard',KEYS[1])
local o={}
if c>cap then
  local r=redis.call('zrange',KEYS[1],cap - c,-1,'WITHSCORES')
  for i,m in ipairs(r) do
    if i % 2 == 1 then
      redis.call('zrem',KEYS[1],m)
      c=c-1
      if m==ARGV[3] then
        y=0
      else
        o[#o+1]=r[i]
        o[#o+1]=r[i+1]
      end
    end
  end
end
return {c,o,y}
"""

_scripts['queue_indexof'] = """
local o={}
local len=redis.call('llen',KEYS[1])
for i=1,#ARGV do
    o[i]=-1
    local j=0
    local indv
    while j<len and indv~=ARGV[i] do
        indv=redis.call('lindex',KEYS[1],j)
        if indv==ARGV[i] then
            o[i]=j
        end
        j=j+1
    end
end
return o
"""

_scripts['priority_queue_indexof'] = """
local o={}
for i=1,#ARGV do
    local r=redis.call('zrank',KEYS[1],ARGV[i])
    if r~=nil then
        o[i]=r
    else
        o[i]=-1
    end
end
return o
"""

_map = {
    # queue
    'queue_push': 'queue_push',
    'queue_push_not_in': 'queue_push_not_in',
    'queue_pop': 'queue_pop',
    'capped_queue_push': 'capped_queue_push',
    'capped_queue_push_not_in': 'capped_queue_push_not_in',
    'capped_queue_pop': 'queue_pop',
    'of_capped_queue_push': 'of_capped_queue_push',
    'of_capped_queue_push_not_in': 'of_capped_queue_push_not_in',
    'of_capped_queue_pop': 'queue_pop',
    'queue_indexof': 'queue_indexof',
    'capped_queue_indexof': 'queue_indexof',
    # deque
    'deque_push_back': 'queue_push',
    'deque_push_back_not_in': 'queue_push_not_in',
    'deque_push_front': 'deque_push_front',
    'deque_push_front_not_in': 'deque_push_front_not_in',
    'deque_pop_back': 'deque_pop_back',
    'deque_pop_front': 'queue_pop',
    'capped_deque_push_front': 'capped_deque_push_front',
    'capped_deque_push_front_not_in': 'capped_deque_push_front_not_in',
    'capped_deque_push_back': 'capped_queue_push',
    'capped_deque_push_back_not_in': 'capped_queue_push_not_in',
    'of_capped_deque_push_front': 'of_capped_deque_push_front',
    'of_capped_deque_push_front_not_in': 'of_capped_deque_push_front_not_in',
    'of_capped_deque_push_back': 'of_capped_queue_push',
    'of_capped_deque_push_back_not_in': 'of_capped_queue_push_not_in',
    'of_capped_deque_pop_front': 'queue_pop',
    'of_capped_deque_pop_back': 'deque_pop_back',
    'deque_indexof': 'queue_indexof',
    'capped_deque_indexof': 'queue_indexof',
    # stack
    'stack_push': 'stack_push',
    'stack_push_not_in': 'stack_push_not_in',
    'stack_pop': 'stack_pop',
    'capped_stack_push': 'capped_stack_push',
    'capped_stack_push_not_in': 'capped_stack_push_not_in',
    'capped_stack_pop': 'stack_pop',
    'stack_indexof': 'queue_indexof',
    # priority queue
    'priority_queue_push': 'priority_queue_push',
    'priority_queue_push_not_in': 'priority_queue_push_not_in',
    'priority_queue_pop': 'priority_queue_pop',
    'capped_priority_queue_push': 'capped_priority_queue_push',
    'capped_priority_queue_push_not_in': 'capped_priority_queue_push_not_in',
    'capped_priority_queue_pop': 'priority_queue_pop',
    'of_capped_priority_queue_push': 'of_capped_priority_queue_push',
    'of_capped_priority_queue_push_not_in': 'of_capped_priority_queue_push_not_in',
    'priority_queue_indexof': 'priority_queue_indexof',
    'capped_priority_queue_indexof': 'priority_queue_indexof',
}

def load(command):
    return _scripts[_map[command]]

