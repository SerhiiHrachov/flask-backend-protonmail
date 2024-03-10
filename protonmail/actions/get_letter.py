from protonmail import By, EC


class GetLetter:
    def __init__(self, driver, wait):
        self.wait = wait
        self.driver = driver
        self.iframe = "//div/iframe"
        self.message_item = "message-container"
        self.recipient_item = "message-recipient-item"
        self.sender_item = "message-header-from-container"
        self.subject_item = "message-conversation-summary-header"
        self.body_script = """return document.evaluate('/html//div[@id="proton-root"]//div[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;"""

    def get_sender(self, soup, id):
        self.soup = soup
        try:
            self.letter = soup.find(
                "article",
                {"class": self.message_item, "data-message-id": id},
            )
            sender = self.letter.find("div", {"class": self.sender_item})
            return sender.find("span", {"class": self.recipient_item}).get(
                "title"
            )
        except Exception as e:
            print(e)
            return None

    def get_delivery_datetime(self):
        try:
            return self.letter.find("time").get("datetime")
        except Exception as e:
            print(e)
            return None

    def get_recipient(self):
        try:
            to = self.letter.find("div", {"id": "message-recipients"})
            return to.find("span", {"class": self.recipient_item}).get("title")
        except Exception as e:
            print(e)
            return None

    def get_subject(self):
        try:
            return self.soup.find("h1", class_=self.subject_item).text
        except Exception as e:
            print(e)
            return None

    def get_body(self):
        try:
            body = self.wait.until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, self.iframe)
                )
            )
            body = self.driver.execute_script(self.body_script)
            return body.get_attribute("outerText")
        except Exception as e:
            print(e)
            return None
