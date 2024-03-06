class GetMail:
    def __init__(self):
        self.recipient_addr = (
            '//*[@data-testid="recipients:partial-recipients-list"]'
        )
        self.mails_locator = "item-container-wrapper"
        self.mail_sender = "item-senders"
        self.mail_subject = "item-subject"
        self.mail = {}

    def get_mail(self, soup) -> list:
        mail = soup.find_all("div", class_=self.mails_locator)
        for i, letter in enumerate(mail, start=1):
            sender = letter.find("div", class_=self.mail_sender).find("span")
            self.sender = sender.find_next("span").get("title")

            subject = letter.find("div", class_=self.mail_subject).find("span")
            self.subject = subject.get("title")

            self.delivery_datetime = letter.find("time").get("datetime")

            self.id = letter.find("div", class_="read")
            if not self.id:
                self.id = letter.find("div", class_="unread").get(
                    "data-element-id"
                )
                sender = (
                    letter.find("div", class_="unread")
                    .find("div", class_="item-senders")
                    .find("span")
                )
                self.sender = sender.find_next("span").find_next("span").text
            else:
                self.id = self.id.get("data-element-id")
            data = {
                "datetime": self.delivery_datetime,
                "sender": self.sender,
                "subject": self.subject,
                "id": self.id,
            }
            self.mail[i] = data
            if self.mail == "None":
                raise Exception("No letter found")
        return [self.mail, {"count": len(self.mail)}]
