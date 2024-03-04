from protonmail import (
    sleep,
    Firefox,
    ActionChains,
    BeautifulSoup,
    WebDriverWait,
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
)
from protonmail.sign_in.signin_page import SignPage
from protonmail.sign_in.home_page import HomePage
from protonmail.actions.send_mail import NewMail
from protonmail.actions.get_inbox import GetMails


class ProtonMail:
    def __init__(self):
        errors = [
            NoSuchElementException,
            ElementNotInteractableException,
            ElementNotVisibleException,
        ]
        self.driver = Firefox(options=None)
        self.wait = WebDriverWait(self.driver, 10, 0.2, errors)
        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.url = "https://mail.proton.me"
        self.delay = 10

    def logining(self, username: str, password: str) -> bool:
        driver = self.driver
        sign_in = SignPage(driver)
        driver.get(url=self.url)
        sign_in.enter_username(username=username)
        sign_in.enter_password(password=password)
        sign_in.click_signin()
        sleep(self.delay)

        homepage = HomePage(driver)
        if homepage.verify_logining(usename=username):
            print("Logining success")
            return True
        return False

    def send_mail(self, recipient: str, subject: str, message: str) -> bool:
        driver = self.driver
        mail = NewMail(driver)
        mail.enter_recipient(recipient=recipient)
        mail.enter_subject(subject=subject)
        mail.enter_message(message=message)
        mail.send_mail
        if mail.validate_sended_mail:
            print("Mail sended")
            sleep(self.delay)
            return True
        return False

    def check_current_url(self, url: str) -> bool:
        if self.driver.current_url == url:
            return True
        return False

    def get_mails(self, url: str) -> list | bool:
        if self.check_current_url(url) is False:
            self.driver.get(url=url)
        sleep(self.delay)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        data = GetMails().get_mails(soup=soup)
        if data:
            return data
        return False

    @property
    def get_inbox(self):
        return self.get_mails(self.url + "/u/0/inbox")

    @property
    def get_outbox(self):
        return self.get_mails(self.url + "/u/0/all-sent")

    @property
    def get_all(self):
        return self.get_mails(self.url + "/u/0/almost-all-mail")

    @property
    def get_unread(self):
        return self.get_mails(self.url + "/u/0/almost-all-mail#filter=unread")

    @property
    def close_session(self) -> bool:
        try:
            self.driver.close()
            self.driver.quit()
            del self.driver
            return True
        except Exception as err:
            print(err)
