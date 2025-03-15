
---

### **2️⃣ Modify Your Python Script (`commit_breakdown.py`)**  
Update your Python script so that it fetches your actual commit breakdown and replaces these placeholders in `README.md`.  

#### **Here’s an updated script:**  
```python
import requests
import os
import json
from datetime import datetime

# GitHub username and repository
USERNAME = "Obaid03"
REPO = "Obaid03"

# GitHub API URL
url = f"https://api.github.com/repos/{USERNAME}/{REPO}/commits"

# Headers for authentication
headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

# Get commit data
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error fetching commits: {response.status_code}")
    exit(1)

commits = response.json()

# Initialize counters
morning, daytime, evening, night = 0, 0, 0, 0
total_commits = len(commits)

# Categorize commits based on time
for commit in commits:
    commit_time = commit["commit"]["author"]["date"]
    hour = datetime.fromisoformat(commit_time[:-1]).hour  # Remove 'Z' from timestamp

    if 6 <= hour < 12:
        morning += 1
    elif 12 <= hour < 18:
        daytime += 1
    elif 18 <= hour < 24:
        evening += 1
    else:
        night += 1

# Calculate percentages
morning_pct = f"{(morning / total_commits) * 100:.2f}%" if total_commits else "0.00%"
daytime_pct = f"{(daytime / total_commits) * 100:.2f}%" if total_commits else "0.00%"
evening_pct = f"{(evening / total_commits) * 100:.2f}%" if total_commits else "0.00%"
night_pct = f"{(night / total_commits) * 100:.2f}%" if total_commits else "0.00%"

# Read README.md
with open("README.md", "r") as file:
    content = file.read()

# Replace placeholders
content = content.replace("{{MORNING_COMMITS}}", str(morning))
content = content.replace("{{MORNING_PERCENTAGE}}", morning_pct)
content = content.replace("{{DAYTIME_COMMITS}}", str(daytime))
content = content.replace("{{DAYTIME_PERCENTAGE}}", daytime_pct)
content = content.replace("{{EVENING_COMMITS}}", str(evening))
content = content.replace("{{EVENING_PERCENTAGE}}", evening_pct)
content = content.replace("{{NIGHT_COMMITS}}", str(night))
content = content.replace("{{NIGHT_PERCENTAGE}}", night_pct)

# Write back to README.md
with open("README.md", "w") as file:
    file.write(content)

print("README.md updated successfully!")
