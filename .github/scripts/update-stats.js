const fs = require('fs');
const { Octokit } = require('@octokit/rest');

async function updateStats() {
  try {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

    // Get commit activity with proper error handling
    const { data } = await octokit.repos.getCommitActivityStats({
      owner: 'Obaid03',
      repo: 'Obaid03'
    });

    if (!Array.isArray(data)) {
      throw new Error('Invalid API response format');
    }

    // Calculate totals safely
    const totalCommits = data.reduce((sum, week) => sum + (week?.total || 0), 0);
    const lastWeekCommits = data.length > 0 ? (data.slice(-1)[0]?.total || 0) : 0;

    // Update README
    const readmePath = './README.md';
    let readme = fs.readFileSync(readmePath, 'utf8');
    
    readme = readme.replace(
      /<!--COMMIT_STATS_START-->[\s\S]*<!--COMMIT_STATS_END-->/,
      `<!--COMMIT_STATS_START-->
### 📊 Real-Time Commit Activity
| Period        | Commits  |
|---------------|----------|
| **All Time**  | ${totalCommits.toLocaleString()} |
| **Last Week** | ${lastWeekCommits.toLocaleString()} |
<!--COMMIT_STATS_END-->`
    );

    fs.writeFileSync(readmePath, readme);
    console.log('Successfully updated stats!');
  } catch (error) {
    console.error('Error updating stats:', error.message);
    process.exit(1);
  }
}

updateStats();
