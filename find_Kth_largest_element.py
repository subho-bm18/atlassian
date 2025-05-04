import heapq

def find_kth_largest(nums, k):
    min_heap = nums[:k]               # O(k)
    heapq.heapify(min_heap)           # O(k)

    for num in nums[k:]:              # O(n - k) iterations
        if num > min_heap[0]:
            heapq.heappushpop(min_heap, num)  # O(log k)

    return min_heap[0]

a = [3, 2, 1, 5, 6, 4, 100, 200, 99, 101]
k = 3
result = find_kth_largest(a, k)
print(f"The {k}th largest element is: {result}")