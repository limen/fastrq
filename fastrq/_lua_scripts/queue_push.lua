local len
for i,k in ipairs(ARGV) do
  len=redis.call('rpush',KEYS[1],k)
end
return len
