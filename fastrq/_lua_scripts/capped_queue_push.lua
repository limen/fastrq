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