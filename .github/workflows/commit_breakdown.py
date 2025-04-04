import requests
import os
from datetime import datetime
import pytz  # Install with `pip install pytz`

# GitHub Username
USERNAME = "Obaid03"

# GitHub API URL for events (tracks all commits across repositories)
API_URL = f"https://api.github.com/users/{USERNAME}/events"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

# Fetch all commit events (handle pagination)
commits = []
page = 1
while True:
    response = requests.get(API_URL, headers=HEADERS, params={"page": page, "per_page": 100})
    if response.status_code != 200:
        print(f"Error fetching commits: {response.status_code}")
        exit(1)
    data = response.json()
    if not data:
        break

    # Extract commits from PushEvents
    for event in data:
        if event["type"] == "PushEvent":
            for commit in event["payload"]["commits"]:
                if commit["author"]["name"] == USERNAME:  # Only count your commits
                    commits.append(commit)

    if len(data) < 100:  # Stop if fewer than 100 events in the last page
        break
    page += 1

# Categorize commits based on time
morning, daytime, evening, night = 0, 0, 0, 0
total_commits = len(commits)

# Set your local time zone (Pakistan)
local_tz = pytz.timezone("Asia/Karachi")

for commit in commits:
    commit_time = commit["timestamp"]
    utc_time = datetime.fromisoformat(commit_time[:-1])  # Convert from UTC
    local_time = utc_time.astimezone(local_tz)  # Convert to Pakistan time
    hour = local_time.hour

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
|  | Time Period | Commits | Progress | Percentage |
|---|---|---|---|---|
| ☀️ | Morning   | {morning} commits | `{progress_bar(morning_pct)}` | {morning_pct} |
| 🌆 | Daytime   | {daytime} commits | `{progress_bar(daytime_pct)}` | {daytime_pct} |
| 🌃 | Evening   | {evening} commits | `{progress_bar(evening_pct)}` | {evening_pct} |
| 🌙 | Night     | {night} commits | `{progress_bar(night_pct)}` | {night_pct} |

_Last updated: {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')}_  
"""

# Update README.md
with open("README.md", "r") as file:
    content = file.read()

start_marker = "<!-- COMMIT_BREAKDOWN_START -->"
end_marker = "<!-- COMMIT_BREAKDOWN_END -->"

# Split the content and preserve everything before and after the markers
before_marker = content.split(start_marker)[0]
after_marker = content.split(end_marker)[1]

# Combine the content with the new commit breakdown
new_content = before_marker + start_marker + commit_breakdown_text + end_marker + after_marker

with open("README.md", "w") as file:
    file.write(new_content)

print("README.md updated successfully!")
