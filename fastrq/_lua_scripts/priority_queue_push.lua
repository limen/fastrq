local i=1
while i < #ARGV do
  redis.call('zadd',KEYS[1],ARGV[i],ARGV[i + 1])
  i=i + 2
end
return redis.call('zcard',KEYS[1])