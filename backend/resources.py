import os
import signal

from flask_restful import Resource
from marshmallow import ValidationError

from protonmail import ProtonMail
from backend.schemas import IdSchema, SendSchema
from backend.parse import signin_post_args, send_post_args
from backend.auth_credendials import auth

proton = ProtonMail()
proton.start_session()


class SignIn(Resource):
    @auth.login_required
    def post(self):
        args = signin_post_args.parse_args()
        success = proton.logining(
            args["username"],
            args["password"],
        )
        if success is False:
            return {"success": success}, 500
        return {"success": success}, 201


class Send(Resource):
    @auth.login_required
    def post(self):
        args = send_post_args.parse_args()
        schema = SendSchema()
        try:
            schema.load(args)
        except ValidationError as err:
            return err.messages, 400

        try:
            success = proton.send_letter(
                args["to"], args["subject"], args["message"]
            )
        except Exception as err:
            return err.args, 500
        if success is False:
            return {"message": "Email not sent"}, 500
        return {"message": "Email sent successfully"}, 201


class Status(Resource):
    def get(self):
        return {"healthy": True}, 201


class Inbox(Resource):
    @auth.login_required
    def get(self):
        inbox = proton.inbox()
        if inbox is False:
            return {"error": "Mails not found"}, 404
        return {"inbox": inbox}, 201


class Outbox(Resource):
    @auth.login_required
    def get(self) -> dict:
        outbox = proton.outbox()
        if outbox is False:
            return {"error": "Mails not found"}, 404
        return {"outbox": outbox}, 201


class Unread(Resource):
    @auth.login_required
    def get(self) -> dict:
        unread = proton.unread_box()
        if unread is False:
            return {"error": "Mails not found"}, 404
        return {"unread": unread}, 201


class All(Resource):
    @auth.login_required
    def get(self) -> dict:
        all = proton.all_box()
        if all is False:
            return {"error": "Mails not found"}, 404
        return {"all": all}, 201


class Shutdown(Resource):
    @auth.login_required
    def get(self):
        close = proton.close_session()
        if close:
            try:
                os.kill(os.getpid(), signal.SIGINT)
                return close
            except Exception as err:
                return err.args, 500
            finally:
                exit(0)


class CloseSession(Resource):
    @auth.login_required
    def get(self) -> dict:
        close = proton.close_session()
        if close is False:
            return {"error": "Session not closed"}, 400
        return {"success": True, "message": "Session closed"}, 201


class ReadMailById(Resource):
    @auth.login_required
    def get(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.get_letter_by_id(id)
        except Exception as err:
            return err.args, 500

        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201


class MarkAsUnread(Resource):
    @auth.login_required
    def put(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.mark_as_unread(id)
        except Exception as err:
            return err.args, 500
        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201


class MarkAsRead(Resource):
    @auth.login_required
    def put(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.mark_as_read(id)
        except Exception as err:
            return err.args, 500
        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201


class Delete(Resource):
    @auth.login_required
    def delete(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.move_to_trash(id)
        except Exception as err:
            return err.args, 500
        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201


class Spam(Resource):
    @auth.login_required
    def put(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.mark_as_spam(id)
        except Exception as err:
            return err.args, 500
        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201


class Archive(Resource):
    @auth.login_required
    def put(self, id: str) -> dict:
        schema = IdSchema()
        try:
            schema.load({"id": id})
        except ValidationError as err:
            return err.messages, 400

        try:
            content = proton.move_to_archive(id)
        except Exception as err:
            return err.args, 500
        if content is False:
            return {"error": "Mail not found"}, 404
        return {id: content}, 201
