from flask_jwt_extended import create_access_token
from app.extensions.db import db

# both are valid since init in models has everything
from app.models import User, Profile
# from app.models.user import User
# from app.models.profile import Profile

class AuthService:

    @staticmethod
    def register_user(data): # use complete data obj rather than just name and password
        if User.query.filter_by(email=data['email']).first(): # for user table, email is unique
            return {"error":"Email already registered"}, 400
        
        new_user = User(email=data['email'])
        new_user.set_password(data['password'])

        # the user and profile creation must be checked both before committing, so:

        db.session.add(new_user)
        db.session.flush() # sends the transaction but does not commit

        new_profile = Profile(
            user_id=new_user.id,
            full_name=data.get('full_name','New User') # set default name if not given
        )
        db.session.add(new_profile)

        try:
            db.session.commit() # put final commit only after checking both user and profile transac.
        except Exception:
            db.session.rollback()
            return {"error":"Database error"}, 500

        return {
            "message":"User registered successfully",
            "user_id":new_user.id
        }, 201


    @staticmethod
    def login_user(data):
        user = User.query.filter_by(email=data['email']).first()

        # should have email id and correct password
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id)) # important to keep string    
            return {"access_token":access_token}, 200
        
        return {"error":"Invalid email or password"}, 401