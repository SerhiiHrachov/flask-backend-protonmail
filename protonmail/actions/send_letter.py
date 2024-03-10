from protonmail import By, EC, Keys


class SendLetter:
    def __init__(self, driver, wait, action):
        self.driver = driver
        self.wait = wait
        self.action = action
        self.new_letter_btn = '//*[@data-testid="sidebar:compose"]'
        self.subject_field = '//*[@data-testid="composer:subject"]'
        self.recipient_field = '//*[@data-testid="composer:to"]'
        self.send_letter_btn = '//*[@data-testid="composer:send-button"]'
        self.notification = '//span[contains(@class,"notification__content")]'
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.new_letter_btn)
                )
            ).click()
        except Exception:
            self.driver.quit()

    def enter_recipient(self, recipient: str):
        self.driver.find_element(By.XPATH, self.recipient_field).send_keys(
            recipient
        )

    def enter_subject(self, subject: str):
        self.driver.find_element(By.XPATH, self.subject_field).send_keys(
            subject
        )

    def enter_message(self, message: str):
        self.action.send_keys(Keys.TAB + message).perform()

    def send_letter(self):
        self.driver.find_element(By.XPATH, self.send_letter_btn).click()

    def validate_sended_letter(self) -> bool:
        validation = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.notification))
        )
        if "Message sent" in validation.text:
            return True
        if "Надсилання повідомлення" in validation.text:
            return True
        return False
