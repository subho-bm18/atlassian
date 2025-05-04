from collections import deque
from threading import Lock

class HitCounter:
    def __init__(self):
        self.hits = deque()
        self.lock = Lock()

    def hit(self, timestamp: int) -> None:
        """Record a new hit at the given timestamp."""
        with self.lock:
            if self.hits and self.hits[-1][0] == timestamp:
                self.hits[-1] = (timestamp, self.hits[-1][1] + 1)
            else:
                self.hits.append((timestamp, 1))
            self._evict_old_hits(timestamp)

    def getHits(self, timestamp: int) -> int:
        """Return the number of hits in the past 5 minutes."""
        with self.lock:
            self._evict_old_hits(timestamp)
            return sum(count for _, count in self.hits)

    def _evict_old_hits(self, current_time: int) -> None:
        """Remove hits older than 5 minutes."""
        while self.hits and self.hits[0][0] <= current_time - 300:
            self.hits.popleft()

counter = HitCounter()
counter.hit(1)
counter.hit(2)
counter.hit(300)
print(counter.getHits(300))  # Output: 3
print(counter.getHits(301))  # Output: 2 (hit at timestamp 1 is now outside the 5-min window)


'''
Certainly! Let's break down the hit() method line by line so you understand its role clearly in the thread-safe HitCounter:

Method:
python
Copy
Edit
def hit(self, timestamp: int) -> None:
    """Record a new hit at the given timestamp."""
This method is used to record a hit (or event) at a specific timestamp, which is assumed to be an integer representing seconds.

-> None indicates that this method does not return anything.

Line:
python
Copy
Edit
with self.lock:
This ensures thread safety by acquiring a mutual exclusion lock.

Only one thread can enter the critical section (the block of code inside with) at a time. This prevents race conditions if multiple threads call hit() simultaneously.

Line:
python
Copy
Edit
if self.hits and self.hits[-1][0] == timestamp:
self.hits is a deque that stores (timestamp, count) pairs.

self.hits[-1][0] gets the last recorded timestamp.

If the last hit in the deque is at the same second as the new timestamp, we just want to increment the count instead of appending a new entry (to save space and reduce unnecessary entries).

Line:
python
Copy
Edit
self.hits[-1] = (timestamp, self.hits[-1][1] + 1)
If the current hit is at the same second as the previous one, this line updates the last tuple to increase the count.

Else block:
python
Copy
Edit
else:
    self.hits.append((timestamp, 1))
If the last recorded timestamp is not the same as the current timestamp, then it's a new second, and we add a new tuple (timestamp, 1) to the deque.

Line:
python
Copy
Edit
self._evict_old_hits(timestamp)
This internal method is called to clean up old entries.

It removes all hits that are older than 300 seconds (5 minutes) from the current timestamp, keeping only relevant hits in the deque.

✅ Summary
This method ensures:

Efficient storage (by collapsing multiple hits at the same second).

Correctness over time (by cleaning up stale data).

Thread safety (via the lock).

'''