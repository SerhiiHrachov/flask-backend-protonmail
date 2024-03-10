import signal
from flask import Flask
from flask_restful import Api
from protonmail import proton
from .resources import (
    SignIn,
    Status,
    Send,
    Inbox,
    Outbox,
    Unread,
    All,
    Shutdown,
    CloseSession,
    ReadMailById,
    MarkAsUnread,
    MarkAsRead,
    Delete,
    Spam,
    Archive,
)


app = Flask(__name__)
api = Api(app, prefix="/api/v1")

api.add_resource(Status, "/health")
api.add_resource(SignIn, "/signin")
api.add_resource(Send, "/send")
api.add_resource(Inbox, "/inbox")
api.add_resource(Outbox, "/outbox")
api.add_resource(Unread, "/unread")
api.add_resource(All, "/all")
api.add_resource(Shutdown, "/shutdown")
api.add_resource(CloseSession, "/close")
api.add_resource(ReadMailById, "/read/<string:id>")
api.add_resource(MarkAsUnread, "/mark/unread/<string:id>")
api.add_resource(MarkAsRead, "/mark/read/<string:id>")
api.add_resource(Delete, "/delete/<string:id>")
api.add_resource(Spam, "/spam/<string:id>")
api.add_resource(Archive, "/archive/<string:id>")


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run()
    signal.pause()
    proton.close_session()
    exit(0)
