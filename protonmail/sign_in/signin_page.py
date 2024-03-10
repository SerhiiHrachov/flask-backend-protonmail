from protonmail import By, EC


class SignPage:

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
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
