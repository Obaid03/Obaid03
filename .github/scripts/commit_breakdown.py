import requests
import os
from datetime import datetime
import pytz  

# GitHub Username & Repository
USERNAME = "Obaid03"
REPO = "Obaid03"

# GitHub API URL
API_URL = f"https://api.github.com/repos/{USERNAME}/{REPO}/commits"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

# Fetch all commits (handle pagination)
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
    commits.extend(data)
    page += 1

# Categorize commits based on time
morning, daytime, evening, night = 0, 0, 0, 0
total_commits = len(commits)

# Set Pakistan time zone
local_tz = pytz.timezone("Asia/Karachi")

for commit in commits:
    commit_time = commit["commit"]["author"]["date"]
    utc_time = datetime.fromisoformat(commit_time[:-1])  
    local_time = utc_time.astimezone(local_tz)  
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

# Function to generate progress bar
def progress_bar(percentage):
    filled = int(float(percentage.strip('%')) // 5)
    return "█" * filled + "░" * (20 - filled)

commit_breakdown_text = f"""
<!-- COMMIT_BREAKDOWN_START -->
### 🕒 Commit Activity Breakdown  

|  | Time Period | Commits | Progress | Percentage |
|---|---|---|---|---|
| ☀️ | Morning   | {morning} | `{progress_bar(percentage(morning))}` | {percentage(morning)} |
| 🌆 | Daytime   | {daytime} | `{progress_bar(percentage(daytime))}` | {percentage(daytime)} |
| 🌃 | Evening   | {evening} | `{progress_bar(percentage(evening))}` | {percentage(evening)} |
| 🌙 | Night     | {night} | `{progress_bar(percentage(night))}` | {percentage(night)} |

_Last updated: {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')} (PKT)_
<!-- COMMIT_BREAKDOWN_END -->
"""

# Update README.md
with open("README.md", "r") as file:
    content = file.read()

start_marker = "<!-- COMMIT_BREAKDOWN_START -->"
end_marker = "<!-- COMMIT_BREAKDOWN_END -->"

if start_marker in content and end_marker in content:
    before_marker = content.split(start_marker)[0]
    after_marker = content.split(end_marker)[1]
    new_content = before_marker + commit_breakdown_text + after_marker

    with open("README.md", "w") as file:
        file.write(new_content)

    print("✅ README.md updated successfully!")
else:
    print("❌ Error: Markers not found in README.md!")
