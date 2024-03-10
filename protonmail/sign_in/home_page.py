class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def verify_logining(self, usename: str) -> bool:
        if usename not in self.driver.title:
            self.driver.quit()
            raise Exception(f"User {usename} is not logged in")
        return True
