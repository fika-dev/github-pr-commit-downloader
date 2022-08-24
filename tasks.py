import requests
from github import Github
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

def parse_commits_from_pr_using_api(github: Github,owner: str, repo: str, pr_number: str) -> list:
  def _get(url: str):
    return github.request(f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits').json()

  def _parse_commit(commit: dict, repo: str, pr_number: str):
    commit_url: str =  commit['html_url']
    sha = commit['sha']
    diff_string = _get_diff_string(commit_url)
    commit_message = commit['commit']['message']
    return {
      'sha': sha,
      'diff_string': diff_string,
      'commit_message': commit_message,
      'commit_url': commit_url,
      'pr_number': pr_number,
      'repo': repo,
    }

  def _get_diff_string(commit_url: str):
    r = requests.get(f'{commit_url}.diff')
    return r.text


  commits = _get( f'https://github.com/{owner}/{repo}/pull/{pr_number}')
  parsed = [_parse_commit(elm, f'{owner}/{repo}', pr_number) for elm in commits]
  return parsed


def parse_commits_from_pr_using_bs(owner: str, repo: str, pr_number: str) -> list:
  def _get(url: str):
    r = requests.get(url)
    if r.status_code == 200:
      return r.text
    else:
      raise 'error'

  def _find_commits(soup: BeautifulSoup) -> list[WebElement]:
    commit_list_candid  = soup.select('div[data-test-selector="pr-timeline-commits-list"]')
    if (len(commit_list_candid)>0):
      commit_list = commit_list_candid[0]
      commits = commit_list.select('div.pr-1>code>a')
      return commits
    else:
      return []

  def _parse_commit(commit_element, repo: str, pr_number: str):
    commit_url: str =  commit_element.attrs['href']
    sha = commit_url.split('/commits/')[-1].strip()
    diff_string = _get_diff_string(commit_url)
    commit_message = commit_element.text
    return {
      'sha': sha,
      'diff_string': diff_string,
      'commit_message': commit_message,
      'commit_url': commit_url,
      'pr_number': pr_number,
      'repo': repo,
    }

  def _get_diff_string(commit_url: str):
    r = requests.get(f'https://github.com{commit_url}.diff')
    return r.text


  doc = _get( f'https://github.com/{owner}/{repo}/pull/{pr_number}')
  soup = BeautifulSoup(doc, 'html.parser')
  commit_elements = _find_commits(soup)
  commits = [_parse_commit(elm, f'{owner}/{repo}', pr_number) for elm in commit_elements]
  return commits



def parse_commits_from_pr(driver: WebDriver, owner: str, repo: str, pr_number: str) -> list:
  def _visit(driver: WebDriver, url: str):
    driver.get(url)
    return 

  def _find_commits(driver: WebDriver) -> list[WebElement]:
    wait = WebDriverWait(driver, 10)
    condition = expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-test-selector="pr-timeline-commits-list"]'))
    commit_list_candid = wait.until(condition)
    if (len(commit_list_candid)>0):
      commit_list : WebElement = commit_list_candid[0]
      commits: list[WebElement] = commit_list.find_elements_by_css_selector('div.pr-1>code>a')
      return commits
    else:
      return []

  def _parse_commit(commit_element: WebElement, repo: str, pr_number: str):
    commit_url: str =  commit_element.get_attribute('href')
    sha = commit_url.split('/commits/')[-1].strip()
    diff_string = _get_diff_string(commit_url)
    commit_message = commit_element.text
    return {
      'sha': sha,
      'diff_string': diff_string,
      'commit_message': commit_message,
      'commit_url': commit_url,
      'pr_number': pr_number,
      'repo': repo,
    }

  def _get_diff_string(commit_url: str):
    r = requests.get(f'{commit_url}.diff')
    return r.text


  _visit(driver, f'https://github.com/{owner}/{repo}/pull/{pr_number}')
  commit_elements = _find_commits(driver)
  commits = [_parse_commit(elm, f'{owner}/{repo}', pr_number) for elm in commit_elements]
  return commits

def get_pr_list(github: Github, owner: str, repo: str):
  def _parse_pr(data):
    return {
      'number': data['number'],
      'url': data['url'],
      'issue_url': data['issue_url'],
      'merged_at': data['merged_at'],
      'merge_commit_sha': data['merge_commit_sha'],
      'user': data['user']['html_url'],
      # 'labels': ', '.join(data['labels']),
      'base': data['base']['ref'],
    }
  pr_remained = True
  total_pr = []
  pr_page_idx = 1
  while pr_remained | pr_page_idx<4:
    pr_list: list = github.request(f'https://api.github.com/repos/{owner}/{repo}/pulls', {
      'per_page': 100,
      'state': 'all',
      'page': pr_page_idx,
    }).json()
    if (len(pr_list) == 0):
      pr_remained = False
    else:
      pr_list = [_parse_pr(pr) for pr in pr_list]
      total_pr = total_pr + pr_list
      print(f'total pr length: {len(total_pr)}')
      pr_page_idx+=1
  return total_pr


