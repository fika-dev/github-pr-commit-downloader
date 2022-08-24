import os
import pickle
from github import Github
from loader import Loader
from saver import Saver
from tqdm import tqdm
 
from tasks import get_pr_list, parse_commits_from_pr_using_api


github = Github()
loader = Loader('data/repos_typescript_starts_100_pr_commit_limit.json')
pr_saver = Saver('../data/pr')
commit_saver = Saver('../data/commit')

if 'repo_ckpt.pkl' in os.listdir():
    with open('repo_ckpt.pkl', 'rb') as f:
        repo_idx, pr_idx = pickle.load(f)
    print(f"Loading from {repo_idx}..{pr_idx}")
else:
  repo_idx = 0
  pr_idx = -1

for i in  range(loader.repo_length):
  if (i >= repo_idx):
    repo = loader.get(i)
    [owner, repo] = repo['name'].split('/')
    pr_list = get_pr_list(github, owner, repo)
    for pr_i, pr in tqdm(enumerate(pr_list)):
      if (pr_i > pr_idx):
        pr_saver.add(pr)
        commits = parse_commits_from_pr_using_api(github, owner, repo, pr['number'], i, pr_i)
        commit_saver.add_all(commits)
        commit_saver.save()
        pr_saver.save()

commit_saver.close()
pr_saver.close()
