from collections import defaultdict
from typing import List

class Solution:
    def rankTeams(self, votes: List[str]) -> str:
        if not votes:
            return ""

        num_teams = len(votes[0])
        vote_counts = defaultdict(lambda: [0] * num_teams)

        # Step 1: Tally votes
        for vote in votes:
            for rank, team in enumerate(vote):
                vote_counts[team][rank] += 1

        # Step 2: Sort teams
        teams = list(votes[0])
        teams.sort(key=lambda team: (vote_counts[team], team), reverse=True)

        return "".join(teams)

if __name__ == "__main__":
    # Example usage
    votes = ["ABC", "ACB", "CAB"]
    solution = Solution()
    print(solution.rankTeams(votes))  # Output: "ACB" 
    