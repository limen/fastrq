local h=redis.call('zrange',KEYS[1],0,tonumber(ARGV[1]) - 1,'WITHSCORES')
local i=1
while i < #h do
  redis.call('zrem',KEYS[1],h[i])
  i=i + 2
end
return h