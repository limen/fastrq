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
