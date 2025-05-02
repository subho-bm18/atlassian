from dataclasses import dataclass
from typing import List
from collections import defaultdict
import threading
import heapq
from concurrent.futures import ThreadPoolExecutor

@dataclass
class File:
    id: str
    size: int
    collection_ids: List[str]

def process_batch(files_batch):
    local_map = defaultdict(int)
    for file in files_batch:
        for cid in file.collection_ids:
            local_map[cid] += file.size
    return local_map

def merge_maps(global_map, local_map, lock):
    with lock:
        for k, v in local_map.items():
            global_map[k] += v

def compute_collection_sizes_multithreaded(files: List[File], top_n: int, num_threads=4):
    global_map = defaultdict(int)
    lock = threading.Lock()
    batch_size = (len(files) + num_threads - 1) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(0, len(files), batch_size):
            batch = files[i:i+batch_size]
            futures.append(executor.submit(process_batch, batch))

        for future in futures:
            local_map = future.result()
            merge_maps(global_map, local_map, lock)

    top_collections = heapq.nlargest(top_n, global_map.items(), key=lambda x: x[1])
    return dict(global_map), top_collections

# Test Data
if __name__ == "__main__":
    files = [
        File(id="f1", size=100, collection_ids=["A"]),
        File(id="f2", size=200, collection_ids=["A", "B"]),
        File(id="f3", size=150, collection_ids=["B"]),
        File(id="f4", size=300, collection_ids=["C"]),
        File(id="f5", size=120, collection_ids=["A", "C"]),
    ]

    total_sizes, top_collections = compute_collection_sizes_multithreaded(files, top_n=2)

    print("Total Sizes by Collection:")
    for cid, size in total_sizes.items():
        print(f"Collection {cid}: {size} bytes")

    print("\nTop Collections:")
    for cid, size in top_collections:
        print(f"Collection {cid}: {size} bytes")
# This code is a multithreaded implementation of the collection size computation.