from protonmail import By, EC


class MenuAction:
    def __init__(self, driver, wait, action):
        self.driver = driver
        self.action = action
        self.wait = wait

    def make(self, id: str, name: str):
        scroll_script = "arguments[0].scrollIntoView(true);"
        btn = f'//*[@data-testid="context-menu-{name}"]'
        data_element_id = f'//*[@data-element-id="{id}"]'

        letter = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, data_element_id))
        )
        # self.action.scroll_to_element(self.letter).perform()
        self.driver.execute_script(scroll_script, letter)
        self.action.context_click(letter).perform()
        self.driver.find_element(By.XPATH, btn).click()

    def trash(self, id: str):
        self.make(id, "trash")
        return "email move to trash"

    def archive(self, id: str):
        self.make(id, "archive")
        return "email move to archive"

    def spam(self, id: str):
        self.make(id, "spam")
        return "email move to spam"

    def unread(self, id: str):
        self.make(id, "unread")
        return "email mark as unread"

    def read(self, id: str):
        self.make(id, "read")
        return "email mark as read"
