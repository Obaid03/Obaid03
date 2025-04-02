const fs = require('fs');
const { Octokit } = require('@octokit/rest');

async function updateStats() {
  try {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
    const { data } = await octokit.repos.getCommitActivityStats({
      owner: 'Obaid03',
      repo: 'Obaid03'
    });

    if (!Array.isArray(data)) throw new Error('API returned non-array data');

    const total = data.reduce((sum, week) => sum + (week?.total || 0), 0);
    const lastWeek = data.slice(-1)[0]?.total || 0;

    const statsTable = `<!--COMMIT_STATS_START-->
### 📊 Commit Activity
| Period       | Commits   |
|--------------|----------|
| All Time     | ${total.toLocaleString()} |
| Last Week    | ${lastWeek.toLocaleString()} |
<!--COMMIT_STATS_END-->`;

    fs.writeFileSync('./README.md', 
      fs.readFileSync('./README.md', 'utf8')
        .replace(/<!--COMMIT_STATS_START-->[\s\S]*<!--COMMIT_STATS_END-->/, statsTable)
    );
    
    console.log('✅ Stats updated successfully');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

updateStats();
