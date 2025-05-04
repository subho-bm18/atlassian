import time
import redis

class SlidingWindowRateLimiter:
    def __init__(self, redis_client, max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def allow_request(self, user_id: str) -> bool:
        now = int(time.time())
        window_start = now - self.window_seconds
        key = f"slidinglog:{user_id}"

        pipeline = self.redis.pipeline()

        # 1. Remove old requests
        pipeline.zremrangebyscore(key, 0, window_start)

        # 2. Get current count after cleanup
        pipeline.zcard(key)

        # 3. Add new request timestamp
        pipeline.zadd(key, {str(now): now})

        # 4. Set expiration for key (optional, keeps Redis clean)
        pipeline.expire(key, self.window_seconds + 60)

        # Execute all in atomic batch
        _, current_count, _, _ = pipeline.execute()

        return current_count < self.max_requests

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
limiter = SlidingWindowRateLimiter(r, max_requests=10, window_seconds=60)

for i in range(12):
    allowed = limiter.allow_request("user123")
    print(f"Request {i+1}: {'✅ Allowed' if allowed else '❌ Denied'}")
    time.sleep(2)
