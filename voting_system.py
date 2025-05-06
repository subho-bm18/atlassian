'''

In a special ranking system, each voter gives a rank from highest to lowest to all teams participating in the competition.

The ordering of teams is decided by who received the most position-one votes. If two or more teams tie in the first position, we consider the second position to resolve the conflict, if they tie again, we continue this process until the ties are resolved. If two or more teams are still tied after considering all positions, we rank them alphabetically based on their team letter.

You are given an array of strings votes which is the votes of all voters in the ranking systems. Sort all teams according to the ranking system described above.

Return a string of all teams sorted by the ranking system.

 

Example 1:

Input: votes = ["ABC","ACB","ABC","ACB","ACB"]
Output: "ACB"
Explanation: 
Team A was ranked first place by 5 voters. No other team was voted as first place, so team A is the first team.
Team B was ranked second by 2 voters and ranked third by 3 voters.
Team C was ranked second by 3 voters and ranked third by 2 voters.
As most of the voters ranked C second, team C is the second team, and team B is the third.
Example 2:

Input: votes = ["WXYZ","XYZW"]
Output: "XWYZ"
Explanation:
X is the winner due to the tie-breaking rule. X has the same votes as W for the first position, but X has one vote in the second position, while W does not have any votes in the second position. 
Example 3:

Input: votes = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]
Output: "ZMNAGUEDSJYLBOPHRQICWFXTVK"
Explanation: Only one voter, so their votes are used for the ranking.
 

Constraints:

1 <= votes.length <= 1000
1 <= votes[i].length <= 26
votes[i].length == votes[j].length for 0 <= i, j < votes.length.
votes[i][j] is an English uppercase letter.
All characters of votes[i] are unique.
All the characters that occur in votes[0] also occur in votes[j] where 1 <= j < votes.length."


To solve this problem, we need to count how many times each team appears in each position, and then sort the teams based on this positional frequency. If there's a tie across all positions, the alphabetical order is used as the final tiebreaker.

✅ Steps to solve:
Initialize a dictionary to store a list of counts for each team. Each list represents the frequency of that team at each position.

Iterate through all votes and for each vote, increment the appropriate position count for the team.

Sort the teams using a custom key:

First by the negative of each position count (since we want descending sort).

Then by alphabetical order if all position counts are equal.
'''


from collections import defaultdict

def rankTeams(votes):
    if not votes:
        return ""

    num_positions = len(votes[0])
    team_counts = defaultdict(lambda: [0] * num_positions)

    # Count how many times each team is voted for each position
    for vote in votes:
        for position, team in enumerate(vote):
            team_counts[team][position] += 1

    # Sort the teams using position counts; if tie, use alphabetical order
    # ✅ Explanation of Sorting Key:
    #The key used in sorting is:

    # lambda team: ([-count for count in team_counts[team]], team)
    # [-count for count in team_counts[team]]: We use negative because Python sorts in ascending order by default, but we want descending frequency.

    # team: Alphabetical tie-breaker.


    sorted_teams = sorted(team_counts.keys(), key=lambda team: ([-count for count in team_counts[team]], team))

    return ''.join(sorted_teams)
# Example usage
votes = ["ABC", "ACB", "ABC", "ACB", "ACB"]
votes1 = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]
result = rankTeams(votes)
print("Ranked teams:", result)