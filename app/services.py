# talks to db/model to get data
# calls utils to perform logic/ check data, call model to save if all good

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token 
from .models import db, User, Profile, Experience
from .utils import check_date_overlap
from datetime import datetime



class ProfileService:

    # Functions to add new Experiences
    @staticmethod
    def add_experience(user_id, data):

        # fetch current profiles
        user = User.query.get(int(user_id))
        if not user or not user.profile: return {"error":"Profile not found"}, 404

        existing_intervals = [(exp.start_date, exp.end_date) for exp in user.profile.experiences]

        try: # schemas checks date but format could still be different
            start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400

        existing_intervals.append((start_date, end_date))

        if check_date_overlap(existing_intervals): # true if overlapping
            return {"error":"Experience dates overlap with existing records"}, 400

        new_exp = Experience(
            profile_id = user.profile.id,
            company = data["company"],
            role = data["role"],
            start_date = start_date,
            end_date = end_date
        )

        db.session.add(new_exp)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback() # undo the current transaction
            return {"error": "Database error"}, 500
        return {"message":"Experience added successfully"}, 201


    @staticmethod
    def get_user_experience(user_id):
        user = User.query.get(int(user_id))
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404

        experiences = []
        for exp in user.profile.experiences:
            experiences.append({
                "id":exp.id,
                "company":exp.company,
                "role":exp.role,
                "start_date":exp.start_date.strftime('%Y-%m-%d'), # since experience table has date format
                "end_date":exp.end_date.strftime('%Y-%m-%d') if exp.end_date else "Present" # since null allowed
            })
        return {"experiences":experiences}, 200
    

    @staticmethod
    def delete_experience(user_id, exp_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Experience not found"}, 404
        
        exp = Experience.query.get(exp_id)
        if not exp or exp.profile_id != user.profile.id:
            return {"error":"Experience not found"}, 404

        db.session.delete(exp)
        db.session.commit()

        return {"message":"Experience deleted succesfullly"}, 200

    @staticmethod
    def get_profile(user_id):
        user = User.query.get(int(user_id))
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        return {
            "full_name":user.profile.full_name,
            "bio":user.profile.bio,
            "email":user.email # since profile does not have email
        }, 200
    

    @staticmethod
    def update_profile(user_id, data):
        user = User.query.get(int(user_id))
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        if "full_name" in data:
            user.profile.full_name = data["full_name"]
        if "bio" in data:
            user.profile.bio = data["bio"]

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"error":"Database error"}, 500
        
        return {"message":"Profile updated successfully"}, 200



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
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token":access_token}, 200
        
        return {"error":"Invalid email or password"}, 401