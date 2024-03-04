from protonmail.proton_mail import ProtonMail

proton = ProtonMail()


def main(username: str, password: str):
    proton.logining(username, password)
    # proton.send_mail("bassdarkside@gmail.com", "VALIDATE", "Test")
    # print(proton.get_inbox)
    # print(proton.get_all)
    # print(proton.get_unread)
    # print(proton.get_outbox)


if __name__ == "__main__":
    main("USERNAME", "PASSWORD")
    proton.close_session
    exit(0)
