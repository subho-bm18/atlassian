import unittest
import time

from ratelimiter_token_bucket_simplified import TokenBucketRateLimiter

class TestTokenBucketRateLimiter(unittest.TestCase):
    def test_allow_within_limit(self):
        rl = TokenBucketRateLimiter(rate=1, capacity=2)
        self.assertTrue(rl.allow_request())
        self.assertTrue(rl.allow_request())
        self.assertFalse(rl.allow_request())  # 3rd request blocked

    def test_allows_after_token_replenishment(self):
        rl = TokenBucketRateLimiter(rate=1, capacity=2)
        rl.allow_request()
        rl.allow_request()
        time.sleep(1.1)  # wait for 1 token to refill
        self.assertTrue(rl.allow_request())

    def test_rate_limiter_respects_capacity(self):
        rl = TokenBucketRateLimiter(rate=5, capacity=3)
        time.sleep(1.0)  # should only fill up to capacity
        self.assertTrue(rl.allow_request())
        self.assertTrue(rl.allow_request())
        self.assertTrue(rl.allow_request())
        self.assertFalse(rl.allow_request())  # 4th request blocked

    def test_zero_capacity(self):
        rl = TokenBucketRateLimiter(rate=1, capacity=0)
        self.assertFalse(rl.allow_request())

if __name__ == '__main__':
    unittest.main()
