from protonmail import (
    print,
    sleep,
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
    def __init__(self):
        errors = [
            NoSuchElementException,
            ElementNotInteractableException,
            ElementNotVisibleException,
        ]
        options = Options()
        options.add_argument("--headless")
        self.driver = Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 10, 0.2, errors)
        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.url = "https://mail.proton.me"
        self.all_mail_url = "https://mail.proton.me/u/0/almost-all-mail"
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

    def send_letter(self, recipient: str, subject: str, message: str) -> bool:
        driver = self.driver
        letter = SendLetter(driver)
        letter.enter_recipient(recipient=recipient)
        letter.enter_subject(subject=subject)
        letter.enter_message(message=message)
        letter.send_letter()
        if letter.validate_sended_letter():
            print("Mail sended")
            sleep(self.delay)
            return True
        return False

    def check_current_url(self, url: str) -> bool:
        if self.driver.current_url == url:
            return True
        return False

    def get_mail_(self, url: str) -> list | bool:
        if self.check_current_url(url) is False:
            self.driver.get(url=url)
        sleep(self.delay)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        data = GetMail().get_mail(soup=soup)
        if data:
            return data
        return False

    def get_mail_by_box(self, box):
        if box == "inbox":
            box = "/inbox"
        elif box == "outbox":
            box = "/all-sent"
        elif box == "all":
            box = "/almost-all-mail"
        elif box == "unread":
            box = "/almost-all-mail#filter=unread"
        return self.get_mail_(self.url + "/u/0" + box)

    def get_letter_by_id(self, id: str) -> dict:
        driver = self.driver
        wait = self.wait
        get_letter = GetLetter(driver, wait)
        url = self.url + "/u/0/almost-all-mail/" + id
        driver.get(url=url)
        sleep(self.delay)
        soup = BeautifulSoup(driver.page_source, "lxml")

        sender = get_letter.get_sender(soup=soup, id=id)
        delivery_datetime = get_letter.get_delivery_datetime()
        recipient = get_letter.get_recipient()
        subject = get_letter.get_subject()
        message = get_letter.get_body()

        if not sender or not delivery_datetime or not recipient or not subject:
            raise Exception("Error")
        return {
            "from": sender,
            "datetime": delivery_datetime,
            "to": recipient,
            "subject": subject,
            "message": message,
        }

    def get_all_mail_page(self):
        driver = self.driver
        wait = self.wait
        action = self.action
        self.menu_action = MenuAction(driver, wait, action)
        if self.check_current_url(self.all_mail_url) is False:
            self.driver.get(self.all_mail_url)

    def move_to_trash(self, id: str):
        self.menu_action.trash(id)

    def move_to_archive(self, id: str):
        self.menu_action.archive(id)

    def mark_as_spam(self, id: str):
        self.menu_action.spam(id)

    def mark_as_unread(self, id: str):
        self.menu_action.unread(id)

    def mark_as_read(self, id: str):
        self.menu_action.read(id)

    def close_session(self) -> bool:
        try:
            self.driver.close()
            self.driver.quit()
            del self.driver
            return True
        except Exception as err:
            print(err)
