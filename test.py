import redis

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 查看所有键
all_keys = r.keys('*')
print("所有键:", all_keys)