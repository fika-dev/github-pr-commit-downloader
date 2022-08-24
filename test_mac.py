from selenium import webdriver

from crawler import Crawler
from tasks import parse_commits_from_pr
chrome_options = webdriver.ChromeOptions()
# options.headless = False
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
path = '/Users/wonmojung/.chrome_drivers/chromedriver_104'
crawler = Crawler(options=chrome_options, path=path, crawler_id='test1', remote=False)
commits = parse_commits_from_pr(crawler.driver, "1milligram", "frontend-tips", "164")
print(len(commits))