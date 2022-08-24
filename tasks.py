from selenium.webdriver.chrome.webdriver import WebDriver
def visit(driver: WebDriver, url: str):
  driver.get(url)
  return 