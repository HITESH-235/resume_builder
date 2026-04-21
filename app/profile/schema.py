from marshmallow import Schema, fields, validate, validates_schema, ValidationError


# ------------------------------------------------------------------------------------
class ProfileUpdateSchema(Schema):
    full_name = fields.Str(required=False, validate=validate.Length(min=1))
    bio = fields.Str(required=False)

    # does not let empty dataset(no updates) return success
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided")


# ------------------------------------------------------------------------------------
class SkillSchema(Schema):
    skills = fields.List(fields.Str(validate=validate.Length(min=1)), required=True, validate=validate.Length(min=1))


# ------------------------------------------------------------------------------------
class ExperienceSchema(Schema):
    company = fields.Str(required=True, validate=validate.Length(min=1))
    role = fields.Str(required=True, validate=validate.Length(min=1))

    start_date = fields.Date(required=True, allow_none=False)
    end_date = fields.Date(allow_none=True) # nullable = allowed

    # checking if interval is valid (start <= end)
    @validates_schema
    def validate_dates(self, data, **kwargs):
        s = data.get("start_date")
        e = data.get("end_date")
        if s and e and s > e:
            raise ValidationError("start_date must be <= end_date")

class ExperienceUpdateSchema(Schema): # differentiates from experienceSchema since req = False here:
    company = fields.Str(required=False, validate=validate.Length(min=1))
    role = fields.Str(required=False, validate=validate.Length(min=1))
    start_date = fields.Date(required=False, allow_none=False)
    end_date = fields.Date(allow_none=True, required=False)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        s = data.get("start_date")
        e = data.get("end_date")
        if s and e and s > e:
            raise ValidationError("start_date must be <= end_date")
        
    # does not let empty dataset(no updates) return success
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided")


# ------------------------------------------------------------------------------------
class EducationSchema(Schema):
    institution = fields.Str(required=True, validate=validate.Length(min=1))
    degree = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    start_date = fields.Date(required=True, allow_none=False)
    end_date = fields.Date(allow_none=True)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        s = data.get("start_date")
        e = data.get("end_date")
        if s and e and s > e:
            raise ValidationError("start_date must be <= end_date")

class EducationUpdateSchema(Schema):
    institution = fields.Str(required=False, validate=validate.Length(min=1))
    degree = fields.Str(required=False, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    start_date = fields.Date(required=False, allow_none=False)
    end_date = fields.Date(allow_none=True, required=False)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        s = data.get("start_date")
        e = data.get("end_date")
        if s and e and s > e:
            raise ValidationError("start_date must be <= end_date")
        
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided")


# ------------------------------------------------------------------------------------
class ProjectSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    role = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    link = fields.Str(allow_none=True)
    start_date = fields.Date(required=True, allow_none=False)
    end_date = fields.Date(allow_none=True)


# ------------------------------------------------------------------------------------
class CertificationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    issuer = fields.Str(required=True, validate=validate.Length(min=1))
    url = fields.Str(allow_none=True)
    date = fields.Date(required=True, allow_none=False)


# ------------------------------------------------------------------------------------
class CourseSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    institution = fields.Str(required=True, validate=validate.Length(min=1))
    date = fields.Date(required=True, allow_none=False)


# ------------------------------------------------------------------------------------
class AchievementSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    date = fields.Date(required=True, allow_none=False)