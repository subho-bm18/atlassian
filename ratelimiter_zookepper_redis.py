import time
import redis
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

# ZooKeeper connection setup
zk = KazooClient(hosts='127.0.0.1:2181')  # Replace with your ZooKeeper ensemble address
zk.start()

# Redis client setup (replace with your Redis nodes if cluster)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

ELECTION_PATH = "/leader_election"

# Create the parent path if it doesn't exist
zk.ensure_path(ELECTION_PATH)

# Redis key for rate limiter (ZSETs for storing requests)
REDIS_KEY_PREFIX = "slidinglog:"

# Configuration for rate limiting
MAX_REQUESTS = 5  # Max requests per user in the time window
WINDOW_SECONDS = 60  # Time window in seconds

# Function to handle the leader election
def leader_election(leader_id):
    """
    Attempts to become the leader for a given user.
    """
    try:
        # Try to create a node in Zookeeper, which represents this node as a leader
        zk.create(f"{ELECTION_PATH}/{leader_id}", value=b"leader", ephemeral=True)
        print(f"{leader_id} is now the leader.")
        return True
    except NodeExistsError:
        print(f"{leader_id} is not the leader yet, waiting...")
        return False


def release_leader(leader_id):
    """
    Release the leader lock when the node goes down or finishes its task.
    """
    zk.delete(f"{ELECTION_PATH}/{leader_id}")
    print(f"{leader_id} has released leadership.")


# Function to update rate limit for a user (in Redis)
def update_rate_limit(user_id, now):
    """
    Updates the rate limit counter for a user in Redis.
    This function should be called by the leader node only.
    """
    key = f"{REDIS_KEY_PREFIX}{user_id}"

    # Use a ZSET to store timestamps for requests
    redis_client.zremrangebyscore(key, 0, now - WINDOW_SECONDS)  # Remove old timestamps
    redis_client.zadd(key, {str(now): now})  # Add current timestamp as a new request

    # Check the count of requests in the last `WINDOW_SECONDS` and enforce the limit
    request_count = redis_client.zcard(key)
    if request_count > MAX_REQUESTS:
        return False  # Rate limit exceeded
    return True


# Function to handle the request
def handle_request(user_id):
    """
    Handle the incoming rate limit request.
    """
    leader_id = f"leader-{user_id}"  # Each user has a unique leader (could be a random leader)
    
    if leader_election(leader_id):
        try:
            now = time.time()
            if update_rate_limit(user_id, now):
                print(f"✅ Request for {user_id} is allowed.")
            else:
                print(f"❌ Request for {user_id} exceeded rate limit.")
        finally:
            release_leader(leader_id)  # Always release leader after processing
    else:
        print(f"Waiting for leader election for {user_id}...")


# Example: Handling requests for multiple users
if __name__ == "__main__":
    for i in range(10):
        handle_request("user123")
        time.sleep(1)  # Simulate time between requests
