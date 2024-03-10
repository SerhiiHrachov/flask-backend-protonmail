from marshmallow import Schema, fields, validate


class SendSchema(Schema):
    to = fields.String(
        required=True, validate=validate.Email(error="Invalid email format!")
    )
    subject = fields.String(
        required=True,
        validate=validate.Length(max=988, error="Subject must be string!"),
    )
    message = fields.String(validate=validate.Length(max=384000))


class IdSchema(Schema):
    id = fields.String(
        required=True,
        validate=validate.Length(equal=88, error="ID must be equal 88 characters"),
    )
