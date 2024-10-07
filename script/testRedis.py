import redis

# 连接到本地 Redis 服务器
r = redis.Redis(host='localhost', port=6379, db=0)

# 连接到远程 Redis 服务器
# r = redis.Redis(host='your_redis_server_ip', port=6379, password='your_redis_password', db=0)

r.set('my_key', 'my_value')

value = r.get('my_key')
print(value)  # 输出：b'my_value'

r.close()