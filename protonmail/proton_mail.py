import os
import logging
from time import sleep
from protonmail import (
    EC,
    Firefox,
    Options,
    ActionChains,
    BeautifulSoup,
    WebDriverWait,
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
)
from protonmail.sign_in.home_page import HomePage
from protonmail.sign_in.signin_page import SignPage
from protonmail.actions.send_letter import SendLetter
from protonmail.actions.get_letter import GetLetter
from protonmail.actions.get_mail import GetMail
from protonmail.actions.make_action import MenuAction


class ProtonMail:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.errors = [
                NoSuchElementException,
                ElementNotInteractableException,
                ElementNotVisibleException,
            ]

            self.url = os.environ.get("PROTONMAIL_URL")
            self.inbox_url = self.url + "/u/0/inbox"
            self.outbox_url = self.url + "/u/0/all-sent"
            self.all_mail_url = self.url + "/u/0/almost-all-mail"
            self.unread_url = self.url + "/u/0/almost-all-mail#filter=unread"
            self.delay = 10
            self.driver = None

    def start_session(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = Firefox(options=options)
        self.wait = WebDriverWait(self.driver, self.delay, 0.2, self.errors)
        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(self.delay)
        self.driver.maximize_window()

    def logining(self, username: str, password: str) -> bool:
        self.start_session()
        driver = self.driver
        wait = self.wait
        sign_in = SignPage(driver, wait)
        driver.get(self.url)
        sign_in.enter_username(username)
        sign_in.enter_password(password)
        sign_in.click_signin()
        wait.until(EC.title_contains(username))
        homepage = HomePage(driver)
        if homepage.verify_logining(username):
            logging.info("Logining success")
            return True
        return False

    def send_letter(self, recipient: str, subject: str, message: str) -> bool:
        driver = self.driver
        wait = self.wait
        action = self.action
        letter = SendLetter(driver, wait, action)
        letter.enter_recipient(recipient)
        letter.enter_subject(subject)
        letter.enter_message(message)
        letter.send_letter()
        if letter.validate_sended_letter():
            logging.info("Mail sending success")
            return True
        return False

    def check_current_url(self, url: str) -> bool:
        if self.driver.current_url == url:
            return True
        return False

    def get_letter_by_id(self, id: str) -> dict:
        driver = self.driver
        wait = self.wait
        get_letter = GetLetter(driver, wait)
        url = self.all_mail_url + "/" + id
        driver.get(url)
        sleep(self.delay)
        soup = BeautifulSoup(driver.page_source, "lxml")

        sender = get_letter.get_sender(soup, id)
        datetime = get_letter.get_delivery_datetime()
        recipient = get_letter.get_recipient()
        subject = get_letter.get_subject()
        message = get_letter.get_body()

        if not sender:
            raise NoSuchElementException("Sender not found")
        if not datetime:
            raise NoSuchElementException("Delivery datetime not found")
        if not recipient:
            raise NoSuchElementException("Recipient not found")
        if not subject:
            raise NoSuchElementException("Subject not found")

        return {
            "from": sender,
            "datetime": datetime,
            "to": recipient,
            "subject": subject,
            "message": message,
        }

    def go_to_page(self):
        driver = self.driver
        wait = self.wait
        action = self.action
        self.menu_action = MenuAction(driver, wait, action)
        if self.check_current_url(self.all_mail_url) is False:
            self.driver.get(self.all_mail_url)

    def move_to_trash(self, id: str):
        self.go_to_page()
        return self.menu_action.trash(id)

    def move_to_archive(self, id: str):
        self.go_to_page()
        return self.menu_action.archive(id)

    def mark_as_spam(self, id: str):
        self.go_to_page()
        return self.menu_action.spam(id)

    def mark_as_unread(self, id: str):
        self.go_to_page()
        return self.menu_action.unread(id)

    def mark_as_read(self, id: str):
        self.go_to_page()
        return self.menu_action.read(id)

    def close_session(self) -> bool:
        try:
            self.driver.close()
            self.driver.quit()
            del self.driver
            return True
        except Exception as err:
            print(err)

    def get_mail(self, url: str) -> list | bool:
        if self.check_current_url(url) is False:
            self.driver.get(url)
            sleep(self.delay)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        data = GetMail().get_mail(soup)
        if data:
            return data
        return False

    def inbox(self):
        return self.get_mail(self.inbox_url)

    def outbox(self):
        return self.get_mail(self.outbox_url)

    def all_box(self):
        return self.get_mail(self.all_mail_url)

    def unread_box(self):
        return self.get_mail(self.unread_url)
