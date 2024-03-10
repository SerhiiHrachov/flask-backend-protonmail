import os
from dotenv import load_dotenv, find_dotenv
from flask_httpauth import HTTPBasicAuth

load_dotenv(find_dotenv())

USER_DATA = {
    os.environ.get("PROTON_USER"): os.environ.get("PROTON_PASS"),
}
auth = HTTPBasicAuth()


@auth.verify_password
def verify(username: str, password: str) -> bool:
    if not (username and password):
        return False
    return USER_DATA.get(username) == password
