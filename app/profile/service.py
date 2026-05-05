from datetime import datetime
from app.models import User, Experience, Skill, Education, Project, Certification, Course, Achievement, CustomItem, ResumeExperience, ResumeEducation, ResumeProject, ResumeCertification, ResumeCourse, ResumeAchievement, ResumeCustomItem
# (otherwise user has backref to profile)
from app.extensions.db import db


class ProfileService:

# --------------------------------------------------------------------------------------------------------------
    # PROFILE methods:

    @staticmethod
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        profile = user.profile
        profile_data = {
            "id": profile.id,
            "full_name": profile.full_name, 
            "email": user.email,
            "bio": profile.bio
        }
        experiences = sorted(
            profile.experiences, 
            key=lambda x: x.start_date
        )
        experiences_data = [
            {
                "id": exp.id,
                "company": exp.company,
                "role": exp.role,
                "start_date": exp.start_date.strftime('%Y-%m-%d'),
                "end_date": exp.end_date.strftime('%Y-%m-%d') if exp.end_date else None
            }
            for exp in experiences
        ]
        educations = sorted(
            profile.educations, 
            key=lambda x: x.start_date
        )
        educations_data = [
            {
                "id": edu.id,
                "institution": edu.institution,
                "degree": edu.degree,
                "description": edu.description,
                "start_date": edu.start_date.strftime('%Y-%m-%d'),
                "end_date": edu.end_date.strftime('%Y-%m-%d') if edu.end_date else None
            }
            for edu in educations
        ]
        skills_data = [{"id": skill.id, "name": skill.name} for skill in profile.skills]
        projects_data = [
            {
                "id": p.id, "name": p.name, "role": p.role, "description": p.description, "link": p.link,
                "start_date": p.start_date.strftime('%Y-%m-%d'),
                "end_date": p.end_date.strftime('%Y-%m-%d') if p.end_date else None
            } for p in profile.projects
        ]
        certifications_data = [
            {
                "id": c.id, "name": c.name, "issuer": c.issuer, "url": c.url,
                "date": c.date.strftime('%Y-%m-%d')
            } for c in profile.certifications
        ]
        courses_data = [
            {
                "id": c.id, "name": c.name, "institution": c.institution,
                "date": c.date.strftime('%Y-%m-%d')
            } for c in profile.courses
        ]
        achievements_data = [
            {
                "id": a.id, "title": a.title, "description": a.description,
                "date": a.date.strftime('%Y-%m-%d')
            } for a in profile.achievements
        ]
        return {
            "status": "success",
            "data": {
                "profile": profile_data,
                "experiences": experiences_data,
                "educations": educations_data,
                "projects": projects_data,
                "certifications": certifications_data,
                "courses": courses_data,
                "achievements": achievements_data,
                "skills": skills_data,
                "custom_items": [
                    {
                        "id": item.id,
                        "title": item.title,
                        "subtitle": item.subtitle,
                        "start_date": item.start_date.strftime('%Y-%m-%d') if item.start_date else None,
                        "end_date": item.end_date.strftime('%Y-%m-%d') if item.end_date else None,
                        "description": item.description,
                        "order": item.order
                    } for item in sorted(profile.custom_items, key=lambda x: x.order)
                ]
            }
        }, 200


    @staticmethod
    def update_profile(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        profile = user.profile
        if "full_name" in data:
            profile.full_name = data["full_name"]
        if "bio" in data:
            profile.bio = data["bio"]
            
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # SKILL functions:

    @staticmethod
    def add_skills(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        profile = user.profile

        skills_input = data.get("skills")

        # check is skills_input is not null and is a list (must be a list)
        if not isinstance(skills_input, list): # equiv. to type(skills_input) == list
            return {"error":"Skills must be a list"}, 400

        added_skills = []
        for skill_name in skills_input:
            # check if not an empty string:
            if not isinstance(skill_name, str) or not skill_name.strip(): continue

            normalised = skill_name.strip().lower()
            skill = Skill.query.filter_by(name=normalised).first()

            if not skill:
                skill = Skill(name=normalised)
                db.session.add(skill)

            if skill not in profile.skills:
                profile.skills.append(skill)
                added_skills.append(normalised) # for debugging

        db.session.commit()

        return {
            "message": "Skills processed", # not "added"
            "added": added_skills # does not show ones that already existed
        }, 200


    @staticmethod
    def delete_skill(user_id, skill_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        skill = Skill.query.get(skill_id)
        if not skill:
            return {"error": "Skill not found"}, 404
            
        if skill in user.profile.skills:
            user.profile.skills.remove(skill)
            db.session.commit()
            return {"message": "Skill removed successfully"}, 200
        return {"error": "Skill not in profile"}, 404


# --------------------------------------------------------------------------------------------------------------
    # EXPERIENCE functions

    @staticmethod
    def add_experience(user_id, data):

        # fetch current profiles
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404

        try: # schemas checks date but format could still be different
            start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400

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
        user = User.query.get(user_id)
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
    def update_experience(user_id, exp_id, data):
        # check if user/profile exists:
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        # check if exp exists and the profile id and exp's foreign key of profile id matches:
        exp = Experience.query.get(exp_id)
        if not exp or exp.profile_id != user.profile.id:
            return {"error":"Experience not found"}, 404

        # check if data has new dates to set:
        try: # prevents wrong format and start_date put to null, 
            if "start_date" in data:
                new_start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            else:
                new_start_date = exp.start_date
            if "end_date" in data:
                new_end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date() if data.get("end_date") else None # set to none if data says so
            else: new_end_date = exp.end_date

        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400

        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400
        
        # update the two finally:
        exp.start_date = new_start_date
        exp.end_date = new_end_date
        
        if "company" in data: exp.company = data["company"]
        if "role" in data: exp.role = data["role"]
        try:
            db.session.commit()
        except Exception:
            db.session.rollback() # undo the current transaction
            return {"error": "Database error"}, 500

        return {"message":"Experience updated successfullly"}, 200


    @staticmethod
    def delete_experience(user_id, exp_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        exp = Experience.query.get(exp_id)
        if not exp or exp.profile_id != user.profile.id:
            return {"error":"Experience not found"}, 404

        # Remove any resume associations first to avoid FK constraint violations
        ResumeExperience.query.filter_by(experience_id=exp_id).delete()

        db.session.delete(exp)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"error": "Database error"}, 500
        
        return {"message":"Experience deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # EDUCATION functions:

    @staticmethod
    def add_education(user_id, data):

        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404

        try:
            start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400

        new_edu = Education(
            profile_id = user.profile.id,
            institution = data["institution"],
            degree = data["degree"],
            description = data.get("description"),
            start_date = start_date,
            end_date = end_date
        )

        db.session.add(new_edu)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"error": "Database error"}, 500
        return {"message":"Education added successfully"}, 201


    @staticmethod
    def get_user_education(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404

        educations = []
        for edu in user.profile.educations:
            educations.append({
                "id":edu.id,
                "institution":edu.institution,
                "degree":edu.degree,
                "description":edu.description,
                "start_date":edu.start_date.strftime('%Y-%m-%d'),
                "end_date":edu.end_date.strftime('%Y-%m-%d') if edu.end_date else "Present"
            })
        return {"educations":educations}, 200


    @staticmethod
    def update_education(user_id, edu_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        edu = Education.query.get(edu_id)
        if not edu or edu.profile_id != user.profile.id:
            return {"error":"Education not found"}, 404

        try:
            if "start_date" in data:
                new_start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            else:
                new_start_date = edu.start_date
            if "end_date" in data:
                new_end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date() if data.get("end_date") else None
            else: new_end_date = edu.end_date

        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400

        except ValueError:
            return {"error":"Invalid date format (YYYY-MM-DD)"}, 400
        
        edu.start_date = new_start_date
        edu.end_date = new_end_date
        
        if "institution" in data: edu.institution = data["institution"]
        if "degree" in data: edu.degree = data["degree"]
        if "description" in data: edu.description = data["description"]
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"error": "Database error"}, 500

        return {"message":"Education updated successfullly"}, 200


    @staticmethod
    def delete_education(user_id, edu_id):
        user = User.query.get(user_id)
        if not user or not user.profile:
            return {"error":"Profile not found"}, 404
        
        edu = Education.query.get(edu_id)
        if not edu or edu.profile_id != user.profile.id:
            return {"error":"Education not found"}, 404

        # Remove any resume associations first to avoid FK constraint violations
        ResumeEducation.query.filter_by(education_id=edu_id).delete()

        db.session.delete(edu)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"error": "Database error"}, 500
        
        return {"message":"Education deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # PROJECT functions:

    @staticmethod
    def add_project(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        profile = user.profile
        item = Project(profile_id=profile.id, **data)
        db.session.add(item)
        db.session.commit()
        return {"message": "Project added successfully", "id": item.id}, 201


    @staticmethod
    def get_user_project(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        items = Project.query.filter_by(profile_id=user.profile.id).all()
        return {"projects": [{c.name: getattr(item, c.name) for c in item.__table__.columns if c.name != 'profile_id'} for item in items]}, 200


    @staticmethod
    def update_project(user_id, item_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Project.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Project not found"}, 404
        for k, v in data.items():
            setattr(item, k, v)
        db.session.commit()
        return {"message": "Project updated successfully"}, 200


    @staticmethod
    def delete_project(user_id, item_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Project.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Project not found"}, 404
        # Remove any resume associations first to avoid FK constraint violations
        ResumeProject.query.filter_by(project_id=item_id).delete()
        db.session.delete(item)
        db.session.commit()
        return {"message": "Project deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # CERTIFICATION functions:

    @staticmethod
    def add_certification(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        profile = user.profile
        item = Certification(profile_id=profile.id, **data)
        db.session.add(item)
        db.session.commit()
        return {"message": "Certification added successfully", "id": item.id}, 201


    @staticmethod
    def get_user_certification(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        items = Certification.query.filter_by(profile_id=user.profile.id).all()
        return {"certifications": [{c.name: getattr(item, c.name) for c in item.__table__.columns if c.name != 'profile_id'} for item in items]}, 200


    @staticmethod
    def update_certification(user_id, item_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Certification.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Certification not found"}, 404
        for k, v in data.items():
            setattr(item, k, v)
        db.session.commit()
        return {"message": "Certification updated successfully"}, 200


    @staticmethod
    def delete_certification(user_id, item_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Certification.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Certification not found"}, 404
        # Remove any resume associations first to avoid FK constraint violations
        ResumeCertification.query.filter_by(certification_id=item_id).delete()
        db.session.delete(item)
        db.session.commit()
        return {"message": "Certification deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # COURSE functions:

    @staticmethod
    def add_course(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        profile = user.profile
        item = Course(profile_id=profile.id, **data)
        db.session.add(item)
        db.session.commit()
        return {"message": "Course added successfully", "id": item.id}, 201


    @staticmethod
    def get_user_course(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        items = Course.query.filter_by(profile_id=user.profile.id).all()
        return {"courses": [{c.name: getattr(item, c.name) for c in item.__table__.columns if c.name != 'profile_id'} for item in items]}, 200


    @staticmethod
    def update_course(user_id, item_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Course.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Course not found"}, 404
        for k, v in data.items():
            setattr(item, k, v)
        db.session.commit()
        return {"message": "Course updated successfully"}, 200


    @staticmethod
    def delete_course(user_id, item_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Course.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Course not found"}, 404
        # Remove any resume associations first to avoid FK constraint violations
        ResumeCourse.query.filter_by(course_id=item_id).delete()
        db.session.delete(item)
        db.session.commit()
        return {"message": "Course deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # ACHIEVEMENT functions:

    @staticmethod
    def add_achievement(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        profile = user.profile
        item = Achievement(profile_id=profile.id, **data)
        db.session.add(item)
        db.session.commit()
        return {"message": "Achievement added successfully", "id": item.id}, 201


    @staticmethod
    def get_user_achievement(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        items = Achievement.query.filter_by(profile_id=user.profile.id).all()
        return {"achievements": [{c.name: getattr(item, c.name) for c in item.__table__.columns if c.name != 'profile_id'} for item in items]}, 200


    @staticmethod
    def update_achievement(user_id, item_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        item = Achievement.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Achievement not found"}, 404
        for k, v in data.items():
            setattr(item, k, v)
        db.session.commit()
        return {"message": "Achievement updated successfully"}, 200


    @staticmethod
    def delete_achievement(user_id, item_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404

        item = Achievement.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Achievement not found"}, 404

        # Remove any resume associations first to avoid FK constraint violations
        ResumeAchievement.query.filter_by(achievement_id=item_id).delete()
        db.session.delete(item)
        db.session.commit()
        return {"message": "Achievement deleted successfully"}, 200


# --------------------------------------------------------------------------------------------------------------
    # CUSTOM-ITEM (Flat) functions:

    @staticmethod
    def add_custom_item(user_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        
        # Determine order
        max_order = db.session.query(db.func.max(CustomItem.order)).filter_by(profile_id=user.profile.id).scalar() or 0
        
        item = CustomItem(
            profile_id=user.profile.id,
            title=data["title"],
            subtitle=data.get("subtitle"),
            description=data.get("description"),
            start_date=datetime.strptime(data["start_date"], '%Y-%m-%d').date() if data.get("start_date") else None,
            end_date=datetime.strptime(data["end_date"], '%Y-%m-%d').date() if data.get("end_date") else None,
            order=data.get("order", max_order + 1)
        )
        db.session.add(item)
        db.session.commit()
        return {"message": "Custom item added", "id": item.id}, 201

    @staticmethod
    def get_user_custom_items(user_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        items = CustomItem.query.filter_by(profile_id=user.profile.id).all()
        return {"custom_items": [
            {
                "id": item.id,
                "title": item.title,
                "subtitle": item.subtitle,
                "start_date": item.start_date.strftime('%Y-%m-%d') if item.start_date else None,
                "end_date": item.end_date.strftime('%Y-%m-%d') if item.end_date else None,
                "description": item.description,
                "order": item.order
            } for item in sorted(items, key=lambda x: x.order)
        ]}, 200

    @staticmethod
    def update_custom_item(user_id, item_id, data):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        
        item = CustomItem.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Item not found"}, 404
        
        if "title" in data: item.title = data["title"]
        if "subtitle" in data: item.subtitle = data["subtitle"]
        if "description" in data: item.description = data["description"]
        if "order" in data: item.order = data["order"]
        
        if "start_date" in data:
            item.start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date() if data["start_date"] else None
        if "end_date" in data:
            item.end_date = datetime.strptime(data["end_date"], '%Y-%m-%d').date() if data["end_date"] else None
            
        db.session.commit()
        return {"message": "Custom item updated"}, 200

    # the order for all other sections are pre designed, only need to order customs items
    @staticmethod
    def reorder_custom_items(user_id, ordered_ids):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        
        items = CustomItem.query.filter_by(profile_id=user.profile.id).all()
        id_to_item = {item.id: item for item in items}
        
        for index, item_id in enumerate(ordered_ids):
            if item_id in id_to_item:
                id_to_item[item_id].order = index + 1
                
        db.session.commit()
        return {"message": "Profile items reordered"}, 200

    @staticmethod
    def delete_custom_item(user_id, item_id):
        user = User.query.get(user_id)
        if not user or not user.profile: return {"error":"Profile not found"}, 404
        
        item = CustomItem.query.filter_by(id=item_id, profile_id=user.profile.id).first()
        if not item: return {"error": "Item not found"}, 404
        
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200