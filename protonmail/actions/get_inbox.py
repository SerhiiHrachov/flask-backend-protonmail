class GetMails:
    def __init__(self):
        self.recipient_addr = (
            '//*[@data-testid="recipients:partial-recipients-list"]'
        )
        self.mails_locator = "item-container-wrapper"
        self.mail_sender = "item-senders"
        self.mail_subject = "item-subject"
        self.mails = {}

    def get_mails(self, soup) -> list:
        mails = soup.find_all("div", class_=self.mails_locator)
        for i, mail in enumerate(mails, start=1):
            sender = mail.find("div", class_=self.mail_sender).find("span")
            self.sender = sender.find_next("span").get("title")

            subject = mail.find("div", class_=self.mail_subject).find("span")
            self.subject = subject.get("title")

            self.delivery_datetime = mail.find("time").get("datetime")

            self.mail_id = mail.find("div", class_="read")
            if not self.mail_id:
                self.mail_id = mail.find("div", class_="unread").get(
                    "data-element-id"
                )
                sender = (
                    mail.find("div", class_="unread")
                    .find("div", class_="item-senders")
                    .find("span")
                )
                self.sender = sender.find_next("span").find_next("span").text
            else:
                self.mail_id = self.mail_id.get("data-element-id")
            data = {
                "delivery_datetime": self.delivery_datetime,
                "sender": self.sender,
                "subject": self.subject,
                "mail_id": self.mail_id,
            }
            self.mails[i] = data
            if self.mails == "None":
                raise Exception("No mails found")
        return [self.mails, {"count": len(self.mails)}]
