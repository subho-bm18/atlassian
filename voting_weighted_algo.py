'''
Vote algorightm - Given votes of candidates sort them by most votes received
First vote have highest weight and subsequent votes have weight-1 then previous vote
Input : [[A, B, C],
[A, C, D],
[D,A,C]]
Output : [A, D , C , B]

🆕 New Problem:
Votes are weighted: First position gets the most points, second gets one less, etc.

The total score for each candidate is what determines the final rank.

New Problem Example
Input:
python
Copy
Edit
votes = [
    ["A", "B", "C"],
    ["A", "C", "D"],
    ["D", "A", "C"]
]
Weighting:
First position = 3 points

Second = 2 points

Third = 1 point

Tally:
Candidate	Total Points
A	3 + 3 + 2 = 8
B	2
C	1 + 2 + 1 = 4
D	1 + 3 = 4

So we get:
A: 8
C: 4
D: 4
B: 2
Break ties alphabetically between C and D → C first.

✅ Expected Output:

["A", "C", "D", "B"]

'''

# This imports defaultdict from the collections module.

# defaultdict is like a normal Python dictionary, but with a default value for missing keys.

# Here, we're using it so that if we reference a candidate for the first time, they automatically start with a score of 0.
from collections import defaultdict

def weighted_vote_ranking_with_scores(votes):
    # Initializes the scoring dictionary.

    # Keys will be candidate names (e.g., "A"), and values will be the total weighted score each candidate receives.
    score = defaultdict(int)
    num_positions = len(votes[0]) # how many positions = vote length

    # Accumulate score based on position weight
    # This defines a function that accepts a list of votes (a list of lists).

    # Each inner list is a ranking from one voter, e.g., ["A", "B", "C"].
    for vote in votes:
    # enumerate() is a built-in Python function that’s very useful when you're looping through a list and need both:

    #     The index (position in the list), and

    #     The value (the actual item at that position)
    # Outer loop: for vote in votes:

    # Goes through each voter's ranking.

    # Example: vote = ["A", "B", "C"]

    # Inner loop: for i, candidate in enumerate(vote):

    # enumerate gives both index i and the candidate at that position.

    # i = 0 → first position, i = 1 → second, etc.


        for i, candidate in enumerate(vote):
            score[candidate] += num_positions - i
# For 3 positions:

# First place → 3 - 0 = 3 points

# Second place → 3 - 1 = 2 points

# Third place → 3 - 2 = 1 point

    # Sort by score (descending), then alphabetically
    # score.items()?
    # score is a dictionary mapping each candidate to their total score.

    # score.items() returns a list of (candidate_name, score) tuples.
    sorted_candidates = sorted(score.items(), key=lambda x: (-x[1], x[0]))
#     x[1] is the score → we put a - in front to sort by descending score

#    x[0] is the candidate name → used as a tie-breaker in ascending (alphabetical)
    # Separate names and scores
    names = [name for name, _ in sorted_candidates]
    scores = {name: s for name, s in sorted_candidates}
    #scores = {name: _ for name, _ in sorted_candidates}

    return names, scores



votes = [
    ["A", "B", "C"],
    ["A", "C", "D"],
    ["D", "A", "C"]
]

ranked_names, ranked_scores = weighted_vote_ranking_with_scores(votes)

print("Ranked candidates:", ranked_names)
print("Scores:", ranked_scores)