from protonmail.proton_mail import ProtonMail

proton = ProtonMail()


def main(username: str, password: str):
    proton.logining(username, password)
    # proton.send_mail("bassdarkside@gmail.com", "VALIDATE", "Test")
    # 'all' 'unread' 'outbox' 'inbox'
    print(proton.get_mail_by_box("outbox"))


if __name__ == "__main__":
    main("USERNAME", "PASSWORD")
    proton.close_session()
    exit(0)
