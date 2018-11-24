_scripts = {}
_scripts['queue_push'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('rpush',KEYS[1],k)
end
return len
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
_scripts['deque_push_front'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('lpush',KEYS[1],k)
end
return len
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
_scripts['stack_push'] = """
local len
for i,k in ipairs(ARGV) do
  len=redis.call('lpush',KEYS[1],k)
end
return len
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
_scripts['priority_queue_push'] = """
local i=1
while i < #ARGV do
  redis.call('zadd',KEYS[1],ARGV[i],ARGV[i + 1])
  i=i + 2
end
return redis.call('zcard',KEYS[1])
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

_map = {
    # queue
    'queue_push': 'queue_push',
    'queue_pop': 'queue_pop',
    'capped_queue_push': 'capped_queue_push',
    'capped_queue_pop': 'queue_pop',
    'of_capped_queue_push': 'of_capped_queue_push',
    'of_capped_queue_pop': 'queue_pop',
    # deque
    'deque_push_back': 'queue_push',
    'deque_push_front': 'deque_push_front',
    'deque_pop_back': 'deque_pop_back',
    'deque_pop_front': 'queue_pop',
    'capped_deque_push_front': 'capped_deque_push_front',
    'capped_deque_push_back': 'capped_queue_push',
    'of_capped_deque_push_front': 'of_capped_deque_push_front',
    'of_capped_deque_push_back': 'of_capped_queue_push',
    'of_capped_deque_pop_front': 'queue_pop',
    'of_capped_deque_pop_back': 'deque_pop_back',
    # stack
    'stack_push': 'stack_push',
    'stack_pop': 'stack_pop',
    'capped_stack_push': 'capped_stack_push',
    'capped_stack_pop': 'stack_pop',
    # priority queue
    'priority_queue_push': 'priority_queue_push',
    'priority_queue_pop': 'priority_queue_pop',
    'capped_priority_queue_push': 'capped_priority_queue_push',
    'capped_priority_queue_pop': 'priority_queue_pop',
    'of_capped_priority_queue_push': 'of_capped_priority_queue_push',
}

def load(command):
    return _scripts[_map[command]]

