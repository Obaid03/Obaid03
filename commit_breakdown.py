import requests
import os
from datetime import datetime

# GitHub Username & Repository
USERNAME = "Obaid03"
REPO = "Obaid03"

# GitHub API URL
API_URL = f"https://api.github.com/repos/{USERNAME}/{REPO}/commits"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

# Fetch commit history
response = requests.get(API_URL, headers=HEADERS)
if response.status_code != 200:
    print(f"Error fetching commits: {response.status_code}")
    exit(1)

commits = response.json()

# Categorize commits based on time
morning, daytime, evening, night = 0, 0, 0, 0
total_commits = len(commits)

for commit in commits:
    commit_time = commit["commit"]["author"]["date"]
    hour = datetime.fromisoformat(commit_time[:-1]).hour  # Convert from UTC

    if 6 <= hour < 12:
        morning += 1
    elif 12 <= hour < 18:
        daytime += 1
    elif 18 <= hour < 24:
        evening += 1
    else:
        night += 1

# Calculate percentages
def percentage(part):
    return f"{(part / total_commits) * 100:.2f}%" if total_commits else "0.00%"

morning_pct = percentage(morning)
daytime_pct = percentage(daytime)
evening_pct = percentage(evening)
night_pct = percentage(night)

# Function to generate progress bar
def progress_bar(percentage):
    filled = int(float(percentage.strip('%')) // 5)  # Each 5% = 1 block
    return "█" * filled + "░" * (20 - filled)

# Generate output text
commit_breakdown_text = f"""
## I'm an Early 🐤

|  | Time Period | Commits | Progress | Percentage |
|---|------------|---------|----------|------------|
| ☀️ | Morning   | {morning} commits | `{progress_bar(morning_pct)}` | {morning_pct} |
| 🌆 | Daytime   | {daytime} commits | `{progress_bar(daytime_pct)}` | {daytime_pct} |
| 🌃 | Evening   | {evening} commits | `{progress_bar(evening_pct)}` | {evening_pct} |
| 🌙 | Night     | {night} commits | `{progress_bar(night_pct)}` | {night_pct} |
"""

# Update README.md
with open("README.md", "r") as file:
    content = file.read()

start_marker = "<!-- COMMIT_BREAKDOWN_START -->"
end_marker = "<!-- COMMIT_BREAKDOWN_END -->"

new_content = content.split(start_marker)[0] + start_marker + commit_breakdown_text + end_marker

with open("README.md", "w") as file:
    file.write(new_content)

print("README.md updated successfully!")
