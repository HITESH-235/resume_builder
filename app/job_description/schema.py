from marshmallow import Schema, fields, validate

class JobDescriptionSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))