from marshmallow import Schema, fields, validate


class UserRegistrationSchema(Schema):
    # fields.Email() checks if the given string has a '@', req=T makes the field non null
    email = fields.Email(required=True) # if the check goes right, 
    # .Str() check for string with non nullable and min length is set by validate.Length()
    password = fields.Str(required=True, validate=validate.Length(min=8))
    full_name = fields.Str(required=False)


# same as registration, with less checks as goes for password check only
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# Alternate (Explicit) way to check validity of data:

# import re # 'regular expression' to check an email

# from datetime import datetime 
# class UserRegistrationSchema2:
#     @staticmethod
#     def validate(data):
#         errors = {} # dictionary with keys that are found with wrong data (value with err msg)

#         email = data.get('email')
#         if not email: errors['email'] = "Email is required"
#         else:
#             email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#             if not re.match(email_pattern, email):
#                 errors['email'] = "Invalid email format"
            
#         password = data.get('password')
#         if not password:
#             errors['password'] = "Password is required"
#         elif len(password) < 8:
#             errors['password'] = 'Passowrd must be atleast 8 characters'

#         return errors