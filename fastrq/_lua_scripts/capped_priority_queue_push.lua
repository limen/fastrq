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
