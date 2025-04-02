const fs = require('fs');
const { Octokit } = require('@octokit/rest');

async function updateStats() {
  try {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

    // Get commits using the newer API endpoint
    const { data: commits } = await octokit.repos.listCommits({
      owner: 'Obaid03',
      repo: 'Obaid03',
      per_page: 100
    });

    // Get last week's timestamp
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    // Count commits
    const totalCommits = commits.length;
    const lastWeekCommits = commits.filter(c => {
      return new Date(c.commit.committer.date) > oneWeekAgo;
    }).length;

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
    console.log('✅ Stats updated successfully!');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

updateStats();
