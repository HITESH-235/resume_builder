from marshmallow import Schema, fields, validate

class ResumeCreateSchema(Schema):
    title = fields.Str(required=True)
    summary = fields.Str()

class AddExperienceSchema(Schema):
    experience_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddSkillSchema(Schema):
    skill_id = fields.Int(required=True)
    order = fields.Int(required=True)

# same for both skills and experience joint table order checking
class ReorderSchema(Schema):
    ordered_ids = fields.List(fields.Int(), required=True)

class UpdateResumeSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1))
    summary = fields.Str(required=False, validate=validate.Length(min=1))