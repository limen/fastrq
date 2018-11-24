local o={}
for i=1,tonumber(ARGV[1]) do
  o[#o + 1]=redis.call('rpop',KEYS[1])
end
return o
