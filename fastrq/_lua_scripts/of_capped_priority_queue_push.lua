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