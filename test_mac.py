from selenium import webdriver

from crawler import Crawler
from tasks import visit
chrome_options = webdriver.ChromeOptions()
# options.headless = False
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
path = '/Users/wonmojung/.chrome_drivers/chromedriver_104'
crawler = Crawler(options=chrome_options, path=path, crawler_id='test1', remote=False)
visit(crawler.driver, "https://github.com/1milligram/frontend-tips/pull/164")
