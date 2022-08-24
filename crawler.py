from selenium import webdriver
class Crawler:
    def __init__(self, crawler_id, options, path, remote=True):
        self.crawler_id = crawler_id
        if (remote):
            self.driver = webdriver.Remote(
                command_executor=path,
                options=options
            )
        else:
            self.driver = webdriver.Chrome(executable_path=path, options=options,)
        

    def __str__(self):
        return self.crawler_id

    def close(self):
        self.driver.close()
    