from flask_restful import reqparse

send_post_args = reqparse.RequestParser()

send_post_args.add_argument(
    "to",
    type=str,
    required=True,
    help="Recipient field is required",
)
send_post_args.add_argument(
    "subject",
    type=str,
    required=True,
    help="Subject field is required",
)
send_post_args.add_argument(
    "message",
    type=str,
)

signin_post_args = reqparse.RequestParser()

signin_post_args.add_argument(
    "username",
    type=str,
    required=True,
    help="Username field is required",
)
signin_post_args.add_argument(
    "password",
    type=str,
    required=True,
    help="Password field is required",
)
