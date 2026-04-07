from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ProfileUpdateSchema(Schema):
    full_name = fields.Str(required=False, validate=validate.Length(min=1))
    bio = fields.Str(required=False)

    # does not let empty dataset(no updates) return success
    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided")
        

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


# separate class for checking errors for data for updation (put req = False)
class ExperienceUpdateSchema(Schema):
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