import time
import redis

RATE_LIMIT_LUA = """
local key = KEYS[1]
local max_tokens = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local data = redis.call("HMGET", key, "tokens", "last_refill")
local tokens = tonumber(data[1]) or max_tokens
local last_refill = tonumber(data[2]) or now

local elapsed = now - last_refill
local refill = math.floor(elapsed * refill_rate)
tokens = math.min(max_tokens, tokens + refill)

if tokens >= 1 then
  tokens = tokens - 1
  redis.call("HMSET", key, "tokens", tokens, "last_refill", now)
  redis.call("EXPIRE", key, 3600)  -- optional: auto-cleanup
  return 1
else
  redis.call("HMSET", key, "tokens", tokens, "last_refill", now)
  return 0
end
"""

class RedisRateLimiter:
    def __init__(self, redis_client, max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.refill_rate = max_requests / window_seconds
        self.lua_script = self.redis.register_script(RATE_LIMIT_LUA)

    def allow_request(self, user_id: str) -> bool:
        now = int(time.time())
        key = f"ratelimit:{user_id}"
        result = self.lua_script(keys=[key],
                                 args=[self.max_requests, self.refill_rate, now])
        return result == 1

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
limiter = RedisRateLimiter(r, max_requests=10, window_seconds=60)

# if limiter.allow_request("user123"):
#     print("✅ Request allowed")
# else:
#     print("❌ Rate limit exceeded")

for i in range(12):
    allowed = limiter.allow_request("user123")
    print(f"Request {i+1}:{'✅ Allowed' if allowed else '❌Denied'}")
    time.sleep(2)  # Simulate time between requests