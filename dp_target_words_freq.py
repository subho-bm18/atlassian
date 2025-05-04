from collections import defaultdict

MOD = 10**9 + 7

def numWays(words, target):
    m, n = len(target), len(words[0])
    
    # Step 1: Count frequency of each character in each column
    count = [defaultdict(int) for _ in range(n)]
    for word in words:
        for col, ch in enumerate(word):
            count[col][ch] += 1

    # Step 2: DP array
    dp = [0] * (m + 1)
    dp[0] = 1  # Base case: one way to form an empty target

    # Step 3: Traverse columns (left to right)
    for col in range(n):
        for i in range(m - 1, -1, -1):
            ch = target[i]
            if ch in count[col]:
                dp[i + 1] += dp[i] * count[col][ch]
                dp[i + 1] %= MOD

    return dp[m]

words = ["EVS", "EGG", "GOD", "EVE", "VEE"]
target = "VEG"
print(numWays(words, target)) 