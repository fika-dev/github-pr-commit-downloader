from selenium import webdriver
from crawler import Crawler
from github import Github
from loader import Loader
from saver import Saver
from tqdm import tqdm
 
from tasks import get_pr_list, parse_commits_from_pr_using_api, parse_commits_from_pr_using_bs
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# path = '/Users/wonmojung/.chrome_drivers/chromedriver_104'
# crawler = Crawler(options=chrome_options, path=path, crawler_id='test1', remote=False)



github = Github()
loader = Loader('data/repos_typescript_starts_100_pr_commit_limit.json')
pr_saver = Saver('/Users/wonmojung/Fika/data/pr')
commit_saver = Saver('/Users/wonmojung/Fika/data/commit')

for i in  range(loader.repo_length):
  repo = loader.get(i)
  [owner, repo] = repo['name'].split('/')
  pr_list = get_pr_list(github, owner, repo)
  for pr in tqdm(pr_list):
    pr_saver.add(pr)
    commits = parse_commits_from_pr_using_api(github, owner, repo, pr['number'])
    commit_saver.add_all(commits)
    commit_saver.save()
    pr_saver.save()

commit_saver.close()
pr_saver.close()
