from protonmail import (
    By,
    EC,
    WebDriverWait,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementNotVisibleException,
)


class SignPage:

    def __init__(self, driver):
        errors = [
            NoSuchElementException,
            ElementNotInteractableException,
            ElementNotVisibleException,
        ]
        self.driver = driver
        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=5,
            poll_frequency=0.2,
            ignored_exceptions=errors,
        )

        self.username_textbox_id = "username"
        self.password_textbox_id = "password"

    def enter_username(self, username: str):
        self.wait.until(
            EC.element_to_be_clickable((By.ID, self.username_textbox_id))
        ).clear()
        self.wait.until(
            EC.element_to_be_clickable((By.ID, self.username_textbox_id))
        ).send_keys(username)
        # self.driver.find_element(By.ID, self.username_textbox_id).clear()
        # self.driver.find_element(By.ID, self.username_textbox_id).send_keys(
        #     username
        # )

    def enter_password(self, password: str):
        self.driver.find_element(By.ID, self.password_textbox_id).clear()
        self.driver.find_element(By.ID, self.password_textbox_id).send_keys(
            password
        )

    def click_signin(self):
        self.driver.find_element(By.ID, self.password_textbox_id).submit()
