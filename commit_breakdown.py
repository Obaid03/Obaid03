import requests
import os
from collections import defaultdict
from datetime import datetime, timezone

# Get environment variables
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Obaid03/Obaid03"  # Change to your actual repo name
URL = f"https://api.github.com/repos/{REPO}/commits"

headers = {"Authorization": f"token {TOKEN}"}
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print("Failed to fetch commits:", response.status_code, response.text)
    exit(1)  # Stop execution if API call fails

commits = response.json()

if not isinstance(commits, list):  # Ensure response is a list
    print("Unexpected API response format:", commits)
    exit(1)

# Dictionary to store commit counts per time of day
commit_times = defaultdict(int)

for commit in commits:
    if not isinstance(commit, dict):
        print("Skipping invalid commit entry:", commit)
        continue
    
    commit_time = commit.get("commit", {}).get("author", {}).get("date")
    if not commit_time:
        print("Skipping commit with missing date:", commit)
        continue
    
    # Convert commit time to UTC hour
    commit_datetime = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    hour = commit_datetime.hour
    
    # Categorize commits by time of day
    if 5 <= hour < 12:
        commit_times["🌞 Morning"] += 1
    elif 12 <= hour < 18:
        commit_times["🌆 Daytime"] += 1
    elif 18 <= hour < 24:
        commit_times["🌃 Evening"] += 1
    else:
        commit_times["🌙 Night"] += 1

# Calculate total commits
total_commits = sum(commit_times.values())

# Generate breakdown text
breakdown_text = "\n## 📊 Commit Breakdown  \n\n```text\n"
for period, count in commit_times.items():
    percentage = (count / total_commits) * 100 if total_commits > 0 else 0
    breakdown_text += f"{period:<25}{count:<10} {percentage:6.2f} %\n"
breakdown_text += "```\n"

# Read current README
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Replace old breakdown with new one
if "## 📊 Commit Breakdown" in readme_content:
    updated_readme = readme_content.split("## 📊 Commit Breakdown")[0] + breakdown_text
else:
    updated_readme = readme_content + "\n" + breakdown_text

# Write updated README
with open("README.md", "w", encoding="utf-8") as file:
    file.write(updated_readme)

print("✅ Commit breakdown updated successfully!")
