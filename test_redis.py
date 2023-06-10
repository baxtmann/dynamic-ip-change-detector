import redis
r = redis.Redis(host="192.168.0.148", port=6379,
                    charset="UTF-8", decode_responses=True, db=0)
redisIPOld = r.get('ip')

print(redisIPOld)