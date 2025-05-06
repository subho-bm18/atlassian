from collections import defaultdict
from typing import List

class Solution:
    def rankTeams(self, votes: List[str]) -> str:
        if not votes:
            return ""

        num_teams = len(votes[0])
        # This sets up a dictionary to count how many times each team received 1st, 2nd, ..., Nth place.

        # For example, if there are 3 teams, each team gets a list like [0, 0, 0], and this list is updated while parsing votes.
        vote_counts = defaultdict(lambda: [0] * num_teams)

        # Step 1: Tally votes
        for vote in votes:
            for rank, team in enumerate(vote):
                vote_counts[team][rank] += 1
        # Loop through each vote string.

        # Use enumerate to know each team's rank in that vote.

        # Increment the appropriate count in vote_counts.

        # So for:
        # votes = ["ABC", "ACB", "ABC", "ACB", "ACB"]
        # The tallied result will be:

        # vote_counts = {
        #     'A': [5, 0, 0],
        #     'B': [0, 2, 3],
        #     'C': [0, 3, 2]
        #     }

        # Step 2: Sort teams
        teams = list(votes[0])
        teams.sort(key=lambda team: (vote_counts[team], team), reverse=True)
        # The sorted team list is joined into a string and returned — e.g., "ACB".
        return "".join(teams)

if __name__ == "__main__":
    # Example usage
    #votes = ["ABC", "ACB", "CAB"]
    votes = ["ABC", "ACB", "ABC", "ACB", "ACB"]
    solution = Solution()
    print(solution.rankTeams(votes))  # Output: "ACB" 
    