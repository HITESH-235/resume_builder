from app.extensions.db import db
from app.models.user import User
from app.models.job_description import JobDescription

class JobDescriptionService:

    @staticmethod
    def create_jd(user_id, data):
        user = User.query.get(user_id)
        if not user: return {"error":"User not found"}, 404
        
        new_jd = JobDescription(
            user_id = user_id,
            title = data["title"],
            content = data["content"]
        )

        db.session.add(new_jd)
        db.session.commit()

        return {"message":"Job Description created successfully"}, 201
    

    @staticmethod
    def get_jds(user_id):
        user = User.query.get(user_id)
        if not user: return {"error":"User not found"}, 404
        
        jds = JobDescription.query.filter_by(user_id=user_id).all()

        res = []
        for jd in jds:
            res.append({
                "id": jd.id,
                "title": jd.title,
                "content": jd.content   
            })

        return {"job_descriptions": res}, 200