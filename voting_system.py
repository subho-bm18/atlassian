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
    sorted_teams = sorted(team_counts.keys(), key=lambda team: ([-count for count in team_counts[team]], team))

    return ''.join(sorted_teams)
# Example usage
votes = ["ABC", "ACB", "ABC", "ACB", "ACB"]
votes1 = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]
result = rankTeams(votes1)
print("Ranked teams:", result)