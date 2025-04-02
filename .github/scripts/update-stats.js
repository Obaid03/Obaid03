const fs = require('fs');
const { Octokit } = require('@octokit/rest');

async function updateStats() {
  // Authenticate
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

  // Get commit activity
  const { data: weeklyStats } = await octokit.repos.getCommitActivityStats({
    owner: 'Obaid03',
    repo: 'Obaid03'
  });

  // Calculate totals
  const totalCommits = weeklyStats.reduce((sum, week) => sum + week.total, 0);
  const lastWeekCommits = weeklyStats.slice(-1)[0].total;

  // Update README
  let readme = fs.readFileSync('./README.md', 'utf8');
  readme = readme.replace(
    /<!--COMMIT_STATS_START-->[\s\S]*<!--COMMIT_STATS_END-->/,
    `<!--COMMIT_STATS_START-->
### 📊 Real-Time Commit Activity
| Period        | Commits  |
|---------------|----------|
| **All Time**  | ${totalCommits} |
| **Last Week** | ${lastWeekCommits} |
<!--COMMIT_STATS_END-->`
  );

  fs.writeFileSync('./README.md', readme);
}

updateStats();
