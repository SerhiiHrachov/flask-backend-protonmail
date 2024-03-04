from protonmail import By, WebDriverWait, ActionChains, EC, Keys


class NewMail:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.action = ActionChains(driver)
        self.new_mail_btn = '//*[@data-testid="sidebar:compose"]'
        self.subject_field = '//*[@data-testid="composer:subject"]'
        self.recipient_field = '//*[@data-testid="composer:to"]'
        self.send_mail_btn = '//*[@data-testid="composer:send-button"]'
        self.notification = '//span[contains(@class,"notification__content")]'
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.new_mail_btn))
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

    @property
    def send_mail(self):
        self.driver.find_element(By.XPATH, self.send_mail_btn).click()

    @property
    def validate_sended_mail(self) -> bool:
        validation = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.notification))
        )
        if "Message sent" in validation.text:
            return True
        if "Надсилання повідомлення" in validation.text:
            return True
        return False
