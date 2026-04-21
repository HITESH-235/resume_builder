from marshmallow import Schema, fields, validate

class ResumeCreateSchema(Schema):
    title = fields.Str(required=True)
    name = fields.Str()
    summary = fields.Str()

class AddSkillSchema(Schema):
    skill_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddExperienceSchema(Schema):
    experience_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddEducationSchema(Schema):
    education_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddProjectSchema(Schema):
    project_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddCertificationSchema(Schema):
    certification_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddCourseSchema(Schema):
    course_id = fields.Int(required=True)
    order = fields.Int(required=True)

class AddAchievementSchema(Schema):
    achievement_id = fields.Int(required=True)
    order = fields.Int(required=True)


# same for both skills and experience joint table order checking
class ReorderSchema(Schema):
    ordered_ids = fields.List(fields.Int(), required=True)

class UpdateResumeSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1))
    name = fields.Str(required=False, allow_none=True)
    summary = fields.Str(required=False, allow_none=True)
    designation = fields.Str(required=False, allow_none=True)
    email = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    location = fields.Str(required=False, allow_none=True)