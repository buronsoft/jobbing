import uuid
from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from jobbing.db import db

class Colony(db.Model):
    __tablename__ = "colony"
    __table_args__ = {'extend_existing': True}
    id_colony_code = db.Column(db.Integer, primary_key=True)
    colony_name = db.Column(db.String(100))
    id_municipality = db.Column(db.Integer)
    id_zip_code = db.Column(db.Integer)

    def __init__(self, id_colony_code:int = None, 
            colony_name:str = None, 
            id_municipality:int = None, 
            id_zip_code:int = None):
        self.id_colony_code = id_colony_code
        self.colony_name = colony_name
        self.id_municipality = id_municipality
        self.id_zip_code = id_zip_code
    
    def __repr__(self):
        return f'<Colony {self.id_colony_code}, {self.colony_name}, {self.id_municipality}, {self.id_zip_code}>'

class CountryCode(db.Model):
    __tablename__ = "country_code"
    __table_args__ = {'extend_existing': True}
    id_country_code = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.Integer)
    country_name = db.Column(db.String(30))

    def __init__(self, id_country_code:int = None, 
            country_code:int = None, 
            country_name:str = None):
        self.id_country_code = id_country_code
        self.country_code = country_code
        self.country_name = country_name
    
    def __repr__(self):
        return f'<CountryCode {self.id_country_code}, {self.country_code}, {self.country_name}>'

class Media(db.Model):
    __tablename__ = "media"
    __table_args__ = {'extend_existing': True}
    media_id = db.Column(db.Integer, primary_key=True)
    media_status_id = db.Column(db.Integer)
    media_data = db.Column(db.LargeBinary)
    media_link = db.Column(db.String(200))
    media_title = db.Column(db.String(30))
    media_description = db.Column(db.String(100))
    media_size = db.Column(db.Float)
    media_content_upload_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    media_content_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python

    def __init__(self, media_id:int = None, 
            media_status_id:int = None, 
            media_data:bin = None, 
            media_link:str = None, 
            media_title:str = None, 
            media_description:str = None, 
            media_size:float = None, 
            media_content_upload_date:str = None, 
            media_content_updated_date:str = None):
        self.media_id = media_id
        self.media_status_id = media_status_id
        self.media_data = media_data
        self.media_link = media_link
        self.media_title = media_title
        self.media_description = media_description
        self.media_size = media_size
        self.media_content_upload_date = media_content_upload_date
        self.media_content_updated_date = media_content_updated_date
    
    def __repr__(self):
        return f'<Media {self.media_id} ,{self.media_status_id}, {self.media_data}, {self.media_link}, {self.media_title}, {self.media_description}, {self.media_size}, {self.media_content_upload_date}, {self.media_content_updated_date}>'

class Municipality(db.Model):
    __tablename__ = "municipality"
    __table_args__ = {'extend_existing': True}
    id_municipality = db.Column(db.Integer, primary_key=True)
    municipality_name = db.Column(db.String(100))
    id_state_code = db.Column(db.Integer)

    def __init__(self, id_municipality:int = None, 
            municipality_name:str = None, 
            id_state_code:int = None):
        self.id_municipality = id_municipality
        self.municipality_name = municipality_name
        self.id_state_code = id_state_code

    def __repr__(self):
        return f'<Municipality {self.id_municipality}, {self.municipality_name}, {self.id_state_code}>' 

class Skills(db.Model):
    __tablename__ = "skills"
    __table_args__ = {'extend_existing': True}
    skills_id = db.Column(db.Integer, primary_key=True)
    skills_name = db.Column(db.String(60))
    skills_media_id = db.Column(db.Integer)
    skills_description = db.Column(db.String(1000)) # FIXME: Max Length of Text in PostgreSQL
    skills_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python

    def __init__(self, skills_id:int = None, 
            skills_name:str = None, 
            skills_media_id:int = None, 
            skills_description:str = None, 
            skills_updated_date:str = None):
        self.skills_id = skills_id
        self.skills_name = skills_name
        self.skills_media_id = skills_media_id
        self.skills_description = skills_description
        self.skills_updated_date = skills_updated_date
    
    def __repr__(self):
        return f'<Skills {self.skills_id}, {self.skills_name}, {self.skills_media_id}, {self.skills_description}, {self.skills_updated_date}>'

class StateCode(db.Model):
    __tablename__ = "state_code"
    __table_args__ = {'extend_existing': True}
    id_state_code = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(3))
    state_name = db.Column(db.String(25))
    id_country_code = db.Column(db.Integer)
    
    def __init__(self, id_state_code:int = None, 
            state_code:str = None, 
            state_name:str = None, 
            id_country_code:int = None):
        self.id_state_code = id_state_code
        self.state_code = state_code
        self.state_name = state_name
        self.id_country_code = id_country_code
    
    def __repr__(self):
        return f'<StateCode {self.id_state_code}, {self.state_code}, {self.state_name}, {self.id_country_code}>'

class Status(db.Model):
    __tablename__ = "status"
    __table_args__ = {'extend_existing': True}
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(15))
    status_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python

    def __init__(self, status_id:int = None, 
            status_name:str = None, 
            status_updated_date:str = None):
        self.status_id = status_id
        self.status_name = status_name
        self.status_updated_date = status_updated_date
    
    def __repr__(self):
        return f'<Status {self.status_id}, {self.status_name}, {self.status_updated_date}>'

class UserAddress(db.Model):
    __tablename__ = "user_address"
    __table_args__ = {'extend_existing': True}
    id_user_address = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(100))
    main_number = db.Column(db.Integer)
    interior_number = db.Column(db.Integer)
    id_colony_code = db.Column(db.Integer)
    id_zip_code = db.Column(db.Integer)
    id_state_code = db.Column(db.Integer)
    id_municipality = db.Column(db.Integer)
    id_country_code = db.Column(db.Integer)
    date_added = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    last_update_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    
    def __init__(self, id_user_address:int = None, 
            street_name:str = None, 
            main_number:int = None, 
            interior_number:int = None, 
            id_colony_code:int = None, 
            id_zip_code:int = None, 
            id_state_code:int = None, 
            id_municipality:int = None, 
            id_country_code:int = None, 
            date_added:str = None, 
            last_update_date:str = None):
        self.id_user_address = id_user_address
        self.street_name = street_name
        self.main_number = main_number
        self.interior_number = interior_number
        self.id_colony_code = id_colony_code
        self.id_zip_code = id_zip_code
        self.id_state_code = id_state_code
        self.id_municipality = id_municipality
        self.id_country_code = id_country_code
        self.date_added = date_added
        self.last_update_date = last_update_date
    
    def __repr__(self):
        return f'<UserAddress {self.id_user_address}, {self.street_name}, {self.main_number}, {self.interior_number}, {self.id_colony_code}, {self.id_zip_code}, {self.id_state_code}, {self.id_municipality}, {self.id_country_code}, {self.date_added}, {self.last_update_date}>'

class UserAuth(UserMixin, db.Model):
    __tablename__ = "user_auth"
    __table_args__ = {'extend_existing': True}
    user_auth_id = db.Column(db.Integer, primary_key=True)
    user_auth_password = db.Column(db.String(500))
    user_auth_pass_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    user_model_id = db.Column(db.Integer)
    user_auth_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    user_auth_name = db.Column(db.String(30))
    user_auth_email = db.Column(db.String(100))

    def __init__(self, user_auth_id:int = None,  
            user_auth_password:str = None, 
            user_auth_pass_date:str = None, 
            user_model_id:int = None, 
            user_auth_updated_date:str = None, 
            user_auth_name:str = None,
            user_auth_email:str = None):
        self.user_auth_id = user_auth_id
        self.user_auth_name = user_auth_name
        self.user_auth_password = generate_password_hash(user_auth_password)
        self.user_auth_pass_date = user_auth_pass_date
        self.user_model_id = user_model_id
        self.user_auth_updated_date = user_auth_updated_date
        self.user_auth_email = user_auth_email
    
    def set_password(self, user_auth_password):
        self.user_auth_password = generate_password_hash(user_auth_password)

    def check_password(self, user_auth_password):
        return check_password_hash(self.user_auth_password, user_auth_password)
    
    def __repr__(self):
        return f'<UserAuth {self.user_auth_id}, {self.user_auth_name}, {self.user_auth_password}, {self.user_auth_pass_date}, {self.user_model_id}, {self.user_auth_updated_date}>'

class UserModel(db.Model):
    __tablename__ = "user_model"
    __table_args__ = {'extend_existing': True}
    user_model_id = db.Column(db.Integer, primary_key=True)
    user_status_id = db.Column(db.Integer)
    user_role_id = db.Column(db.Integer)
    user_model_first_name = db.Column(db.String(100))
    user_model_last_name = db.Column(db.String(100))
    user_model_surname = db.Column(db.String(100))
    user_model_birthday = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    user_model_phone_number = db.Column(db.String(18))
    user_model_address_id = db.Column(db.Integer)
    user_model_registry_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    user_model_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python
    user_model_media_id = db.Column(db.Integer)
    user_model_org = db.Column(db.Integer)
    user_model_creator_id = db.Column(db.Integer)
    user_model_description = db.Column(db.String(300))

    def __init__(self, user_model_id:int = None,
            user_status_id:int = None,
            user_role_id:int = None, 
            user_model_first_name:str = None, 
            user_model_last_name:str = None, 
            user_model_surname:str = None,
            user_model_birthday:str = None, 
            user_model_phone_number:str = None, 
            user_model_address_id:int = None,
            user_model_registry_date:str = None, 
            user_model_updated_date:str = None, 
            user_model_media_id:int = None, 
            user_model_org:int = None, 
            user_model_creator_id:int = None, 
            user_model_description:str = None
            ):
        self.user_model_id = user_model_id
        self.user_status_id = user_status_id
        self.user_role_id = user_role_id
        self.user_model_first_name = user_model_first_name
        self.user_model_last_name = user_model_last_name
        self.user_model_surname = user_model_surname
        self.user_model_birthday = user_model_birthday
        self.user_model_phone_number = user_model_phone_number
        self.user_model_address_id = user_model_address_id
        self.user_model_registry_date = user_model_registry_date
        self.user_model_updated_date = user_model_updated_date
        self.user_model_media_id = user_model_media_id
        self.user_model_org = user_model_org
        self.user_model_creator_id = user_model_creator_id
        self.user_model_description = user_model_description

    def __repr__(self):
        return f'<UserModel {self.user_model_id}, {self.user_status_id}, {self.user_role_id}, {self.user_model_first_name}, {self.user_model_last_name}, {self.user_model_surname}, {self.user_model_birthday}, {self.user_model_phone_number}, {self.user_model_address_id}, {self.user_model_registry_date}, {self.user_model_updated_date}, {self.user_model_media_id}, {self.user_model_org}, {self.user_model_creator_id}, {self.user_model_description}>'

class UserRole(db.Model):
    __tablename__ = "user_role"
    __table_args__ = {'extend_existing': True}
    user_role_id = db.Column(db.Integer, primary_key=True)
    user_role_name = db.Column(db.String(20))
    user_role_updated_date = db.Column(db.String(50)) # FIXME: Timestamp to Date in Python

    def __init__(self, user_role_id:int = None, 
            user_role_name:str = None, 
            user_role_updated_date:str = None):
        self.user_role_id = user_role_id
        self.user_role_name = user_role_name
        self.user_role_updated_date = user_role_updated_date
    
    def __repr__(self):
        return f'<UserRole {self.user_role_id}, {self.user_role_name}, {self.user_role_updated_date}>'

class ZipCode(db.Model): 
    __tablename__ = "zip_code"
    __table_args__ = {'extend_existing': True}
    id_zip_code = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(10))
    
    def __init__(self, id_zip_code:int = None, 
            zip_code:str = None):
        self.id_zip_code = id_zip_code
        self.zip_code = zip_code

    def __repr__(self):
        return f'<ZipCode {self.id_zip_code}, {self.zip_code}>'

class Org(db.Model):
    __tablename__ = "org"
    __table_args__ = {'extend_existing': True}
    org_id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(30))
    org_media_id = db.Column(db.Integer)

    def __init__(self, org_id:int=None, 
            org_name:str=None, 
            org_media_id:int=None):
        self.org_id = org_id
        self.org_name = org_name
        self.org_media_id = org_media_id
    
    def __repr__(self):
        return f'<Org {self.org_id}, {self.org_name}, {self.org_media_id}>'

'''
-------------------------------------------------------------
@author: David Lopez
@date: February 05, 2022
-------------------------------------------------------------
'''

class Profession(db.Model):
    __tablename__ = "profession"
    __table_args__ = {'extend_existing': True}
    profession_id = db.Column(db.Integer, primary_key=True)
    profession_user = db.Column(db.Integer)
    profession_skill = db.Column(db.Integer)

    def __init__(self, profession_id:int=None, 
            profession_user:int=None, 
            profession_skill:int=None):
        self.profession_id = profession_id
        self.profession_user = profession_user
        self.profession_skill = profession_skill
    
    def __repr__(self):
        return f'<Profession {self.profession_id}, {self.profession_user}, {self.profession_skill}>'

class Evidence(db.Model):
    __tablename__ = "evidence"
    __table_args__ = {'extend_existing': True}
    evidence_id = db.Column(db.Integer, primary_key=True)
    evidence_profession = db.Column(db.Integer)
    evidence_media = db.Column(db.Integer)

    def __init__(self, evidence_id:int=None, 
            evidence_profession:int=None, 
            evidence_media:int=None):
        self.evidence_id = evidence_id
        self.evidence_profession = evidence_profession
        self.evidence_media = evidence_media
    
    def __repr__(self):
        return f'<Evidence {self.evidence_id}, {self.evidence_profession}, {self.evidence_media}>'



'''
-------------------------------------------------------------
@author: David Lopez
@date: February 08, 2022
-------------------------------------------------------------
'''

class WorkingArea(db.Model):
    __tablename__ = "working_area"
    __table_args__ = {'extend_existing': True}
    working_area_id = db.Column(db.Integer, primary_key=True)
    working_area_user = db.Column(db.Integer)
    working_area_municipality = db.Column(db.Integer)

    def __init__(self, working_area_id:int=None, 
            working_area_user:int=None, 
            working_area_municipality:int=None):
        self.working_area_id = working_area_id
        self.working_area_user = working_area_user
        self.working_area_municipality = working_area_municipality
    
    def __repr__(self):
        return f'<WorkingArea {self.working_area_id}, {self.working_area_user}, {self.working_area_municipality}>'