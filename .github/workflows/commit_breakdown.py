import requests
import datetime
import os

# GitHub username and repository
USERNAME = "YourGitHubUsername"
REPO = "YourRepositoryName"

# GitHub API URL
API_URL = f"https://api.github.com/repos/{USERNAME}/{REPO}/commits"

# Fetch commits
response = requests.get(API_URL)
commits = response.json()

# Time categories
morning, daytime, evening, night = 0, 0, 0, 0

# Process each commit
for commit in commits:
    commit_time = commit["commit"]["author"]["date"]
    commit_hour = datetime.datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ").hour

    if 6 <= commit_hour < 12:
        morning += 1
    elif 12 <= commit_hour < 18:
        daytime += 1
    elif 18 <= commit_hour < 24:
        evening += 1
    else:
        night += 1

# Total commits
total_commits = morning + daytime + evening + night

# Calculate percentages
morning_pct = (morning / total_commits) * 100
daytime_pct = (daytime / total_commits) * 100
evening_pct = (evening / total_commits) * 100
night_pct = (night / total_commits) * 100

# Update README.md
README_PATH = "README.md"

with open(README_PATH, "r") as file:
    content = file.readlines()

# Find and replace existing commit breakdown
start_index = content.index("### 🌱 My GitHub Activity Breakdown\n") + 2
content[start_index : start_index + 4] = [
    f"| 🌞 Morning  | {morning}   | {morning_pct:.2f}% |\n",
    f"| 🌆 Daytime  | {daytime}   | {daytime_pct:.2f}% |\n",
    f"| 🌃 Evening  | {evening}   | {evening_pct:.2f}% |\n",
    f"| 🌙 Night    | {night}   | {night_pct:.2f}% |\n",
]

# Write updated content
with open(README_PATH, "w") as file:
    file.writelines(content)
