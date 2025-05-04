from collections import deque

class HitCounter:
    def __init__(self):
        # Queue to store (timestamp, count) tuples
        self.hits = deque()

    def hit(self, timestamp: int) -> None:
        """Record a new hit at the given timestamp."""
        if self.hits and self.hits[-1][0] == timestamp:
            # Increment count for the same timestamp
            self.hits[-1] = (timestamp, self.hits[-1][1] + 1)
        else:
            # Append new timestamp with count 1
            self.hits.append((timestamp, 1))
        self._evict_old_hits(timestamp)

    def getHits(self, timestamp: int) -> int:
        """Return the number of hits in the past 5 minutes."""
        self._evict_old_hits(timestamp)
        return sum(count for _, count in self.hits)

    def _evict_old_hits(self, current_time: int) -> None:
        """Remove hits that are older than 5 minutes (300 seconds)."""
        while self.hits and self.hits[0][0] <= current_time - 300:
            self.hits.popleft()

counter = HitCounter()
counter.hit(1)
counter.hit(2)
counter.hit(300)
print(counter.getHits(300))  # Output: 3
print(counter.getHits(301))  # Output: 2 (hit at timestamp 1 is now outside the 5-min window)
