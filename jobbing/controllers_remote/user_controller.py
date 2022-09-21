from flask import abort, make_response, Response
from flask import current_app, jsonify
from flask_login import logout_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash
import connexion
import jwt
from datetime import datetime, timedelta
from jobbing.login import login_manager, token_required

from jobbing.db import db

# DB Models
from jobbing.DBModelsRemote import UserModel as DBUserModel
from jobbing.DBModelsRemote import UserAuth as DBUserAuth
from jobbing.DBModelsRemote import UserAddress as DBUserAddress
from jobbing.DBModelsRemote import UserRole as DBUserRole
from jobbing.DBModelsRemote import Media as DBMedia
from jobbing.DBModelsRemote import Profession as DBProfession
from jobbing.DBModelsRemote import Evidence as DBEvidence
from jobbing.DBModelsRemote import WorkingArea as DBWorkingArea

# Swagger Models
from jobbing.models_remote.user_model import UserModel # noqa: E501
from jobbing.models_remote.user_auth import UserAuth # noqa: E501
from jobbing.models_remote.user_address import UserAddress # noqa: E501
from jobbing.models_remote.user_role import UserRole # noqa: E501
from jobbing.models_remote.media import Media # noqa: E501
from jobbing.models_remote.profession import Profession # noqa: E501
from jobbing.models_remote.evidence import Evidence # noqa: E501
from jobbing.models_remote.working_area import WorkingArea # noqa: E501
from jobbing.models_remote.public_user_model import PublicUserModel # noqa: E501


"""
GET /users
"""
@token_required
def get_users(): # noqa: E501
    """get_users

    Show a listing of users # noqa: E501

    :rtype: List[UserModel]
    """
    
    users = DBUserModel.query.all()
    if users == None:
        abort(404)
    return [UserModel(
        u.user_model_id, 
        u.user_status_id, 
        u.user_role_id, 
        u.user_model_first_name, 
        u.user_model_last_name, 
        u.user_model_surname, 
        u.user_model_birthday, 
        u.user_model_phone_number, 
        u.user_model_address_id, 
        u.user_model_registry_date, 
        u.user_model_updated_date, 
        u.user_model_media_id, 
        u.user_model_org, 
        u.user_model_creator_id,
        u.user_model_description, 
        get_user_professions(u.user_model_id), 
        get_user_working_areas(u.user_model_id)) for u in users]

"""
GET /users/:id
"""
@token_required
def get_user_by_id(user_model_id): # noqa: E501
    """get_user_by_id

    Get user by id # noqa: E501

    :rtype: UserModel
    """

    u = DBUserModel.query.filter(DBUserModel.user_model_id == user_model_id).first()
    if u == None:
        abort(404)
    return UserModel(
        u.user_model_id, 
        u.user_status_id, 
        u.user_role_id, 
        u.user_model_first_name, 
        u.user_model_last_name, 
        u.user_model_surname, 
        u.user_model_birthday, 
        u.user_model_phone_number, 
        u.user_model_address_id, 
        u.user_model_registry_date, 
        u.user_model_updated_date, 
        u.user_model_media_id, 
        u.user_model_org, 
        u.user_model_creator_id, 
        u.user_model_description,
        get_user_professions(u.user_model_id), 
        get_user_working_areas(u.user_model_id))

"""
GET /users/:id/auth
"""
@token_required
def get_user_auth_by_id(user_model_id): # noqa: E501
    """get_user_auth_by_id

    Get user auth info by id # noqa: E501

    :rtype: UserAuth
    """
    
    auth = DBUserAuth.query.filter(DBUserAuth.user_model_id == user_model_id).first()
    if auth == None:
        abort(404)
    return UserAuth(
        auth.user_auth_id, 
        auth.user_auth_password, 
        auth.user_auth_pass_date, 
        auth.user_model_id, 
        auth.user_auth_updated_date, 
        auth.user_auth_name)

"""
GET /users/:id/address
"""
@token_required
def get_user_address_by_id(user_model_id): # noqa: E501
    """get_user_address_by_id

    Get user address info by id # noqa: E501

    :rtype: UserAddress
    """

    user_model = DBUserModel.query.filter(DBUserModel.user_model_id == user_model_id).first()
    if user_model == None:
        abort(404)
    address = DBUserAddress.query.filter(DBUserAddress.id_user_address == user_model.user_model_address_id).first()
    if address == None:
        abort(404)
    return UserAddress(address.id_user_address, 
        address.street_name, 
        address.main_number, 
        address.interior_number, 
        address.id_colony_code, 
        address.id_zip_code, 
        address.id_state_code, 
        address.id_municipality, 
        address.id_country_code, 
        address.date_added, 
        address.last_update_date)

"""
GET users/:id/media
"""
def get_user_media_by_id(user_model_id): # noqa: E501
    """get_user_address_by_id

    Get user media info by id (profile picture) # noqa: E501

    :rtype: Media
    """

    user_model = DBUserModel.query.filter(DBUserModel.user_model_id == user_model_id).first()
    if user_model == None:
        abort(404)
    media = DBMedia.query.filter(DBMedia.media_id == user_model.user_model_media_id).first()
    if media == None:
        abort(404)
    return Media(media.media_id, 
        media.media_status_id, 
        media.media_data.decode("utf-8"), 
        media.media_link, 
        media.media_title, 
        media.media_description, 
        media.media_size, 
        media.media_content_upload_date, 
        media.media_content_updated_date)

"""
GET /users/filter

params:
user_rol_id: int
status_id: int
skill_id: int
"""
@token_required
def get_users_with_filter(user_role_id=None, status_id=None, skill_id=None): # noqa: E501
    """get_users_with_filter

    Get users with filter # noqa: E501

    :rtype: List[UserModel]
    """

    users = DBUserModel.query.filter(
        (DBUserModel.user_role_id == user_role_id if user_role_id is not None else True), 
        (DBUserModel.user_status_id == status_id if status_id is not None else True)).all()

    if skill_id is not None:
        # Filter skill
        users = filter(lambda user: (len(
            set(skill_id) & set([p.profession_skill for p in get_user_professions(user.user_model_id)])) > 0
        ), users)

    if users == None:
        abort(404)
    return [UserModel(
        u.user_model_id, 
        u.user_status_id, 
        u.user_role_id, 
        u.user_model_first_name, 
        u.user_model_last_name, 
        u.user_model_surname, 
        u.user_model_birthday, 
        u.user_model_phone_number, 
        u.user_model_address_id,  
        u.user_model_registry_date, 
        u.user_model_updated_date, 
        u.user_model_media_id, 
        u.user_model_org, 
        u.user_model_creator_id,
        u.user_model_description, 
        get_user_professions(u.user_model_id), 
        get_user_working_areas(u.user_model_id)) for u in users]

"""
POST /login 
"""
def login(body): # noqa: E501
    if not body or not body["user_auth_name"] or not body["user_auth_password"]:
        # returns 401 if any email or / and password is missing
        return make_response('Could not verify', 401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    user = DBUserAuth.query.filter(DBUserAuth.user_auth_name == body["user_auth_name"]).first()
    if not user:
        # returns 401 if user does not exist
        return make_response('Could not verify', 401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.user_auth_password, body['user_auth_password']):
        # generates the JWT Token
        token = jwt.encode({
            'uid': user.user_auth_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, current_app.secret_key, algorithm="HS256")

        # FIXME: Flask login session
        # login_user(user, remember=True)

        return make_response(jsonify({
            'token' : token, 
            'user_model_id': user.user_model_id, 
            'user_auth_id': user.user_auth_id}), 201)

"""
PUT /users

body:
UserModel
"""
@token_required
def put_user(body): # noqa: E501
    """put_user

    Update user # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        # new user model
        body = UserModel.from_dict(connexion.request.get_json())
        print(body)
        
        # old user model
        user_model = get_user_by_id(body.user_model_id)
        if user_model is None:
            abort(404)

        # Only if the row exists
        db.session.query(DBUserModel).filter(DBUserModel.user_model_id == body.user_model_id).update(
            {DBUserModel.user_status_id: body.user_status_id, 
            DBUserModel.user_role_id: body.user_role_id, 
            DBUserModel.user_model_first_name: body.user_model_first_name, 
            DBUserModel.user_model_last_name: body.user_model_last_name, 
            DBUserModel.user_model_surname: body.user_model_surname, 
            DBUserModel.user_model_birthday: body.user_model_birthday, 
            DBUserModel.user_model_phone_number: body.user_model_phone_number, 
            DBUserModel.user_model_address_id: body.user_model_address_id,  
            DBUserModel.user_model_media_id: body.user_model_media_id, 
            DBUserModel.user_model_org: body.user_model_org, 
            DBUserModel.user_model_creator_id: body.user_model_creator_id,
            DBUserModel.user_model_description: body.user_model_description}, synchronize_session="fetch")

        for profession in user_model.user_model_professions:
            # old profession in the new professions list
            if profession.profession_skill in [p.profession_skill for p in body.user_model_professions]:
                new_profession = list(filter(lambda pro: pro.profession_skill == profession.profession_skill, body.user_model_professions))[0]
                put_profession(new_profession)
            # old profession not in the new professions list -> Remove Profession
            else:
                delete_profession(profession.profession_id)
        
        for profession in body.user_model_professions:
            # new profession not in the old professions list -> Add Profession
            if not profession.profession_skill in [p.profession_skill for p in user_model.user_model_professions]:
                post_user_profession(body.user_model_id, profession)

        for area in user_model.user_model_working_areas:
            # old working area not in the new working areas list -> Remove working area
            if not area.working_area_municipality in [a.working_area_municipality for a in body.user_model_working_areas]:
                delete_working_area(area.working_area_id)
        
        for area in body.user_model_working_areas:
            # new working area not in the old working areas list -> Add working area 
            if not area.working_area_municipality in [a.working_area_municipality for a in user_model.user_model_working_areas]:
                post_user_working_area(body.user_model_id, area)

        db.session.commit()
        return (Response(), 201)

    return (Response(), 401)

"""
PUT /professions

body:
Profession
"""
@token_required
def put_profession(body):
    """put_profession

    Update Profession # noqa: E501
    
    :rtype: Response
    """

    if connexion.request.is_json:
        # new profession
        if type(body) is not Profession: 
            body = Profession.from_dict(connexion.request.get_json())

        profession_db = DBProfession.query.filter(DBProfession.profession_id == body.profession_id).first()
        # old profession
        profession = Profession(
            profession_id = profession_db.profession_id, 
            profession_skill = profession_db.profession_skill,
            profession_evidences = get_evidences_profession(profession_db.profession_id)
        )

        for evidence in profession.profession_evidences:
            # old evidence not in new profession evidences -> Remove Evidence
            if not evidence.evidence_media in [e.evidence_media for e in body.profession_evidences]:
                delete_evidence(evidence.evidence_id)

        for evidence in body.profession_evidences:
            # new evidence not in old profession evidences -> Add Evidence
            if not evidence.evidence_media in [e.evidence_media for e in profession.profession_evidences]:
                post_profession_evidence(profession.profession_id, evidence)
        
        db.session.commit()
        return (Response(), 201)

    return (Response(), 401)    

"""
POST /users

body:
UserModel
"""
@token_required
def post_user(body): # noqa: E501
    """post_user

    Create user # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        body = UserModel.from_dict(connexion.request.get_json())

        user = DBUserModel(
            user_status_id = body.user_status_id, 
            user_role_id = body.user_role_id, 
            user_model_first_name = body.user_model_first_name, 
            user_model_last_name = body.user_model_last_name, 
            user_model_surname = body.user_model_surname, 
            user_model_birthday = body.user_model_birthday, 
            user_model_phone_number = body.user_model_phone_number, 
            user_model_address_id = body.user_model_address_id,
            user_model_media_id = body.user_model_media_id, 
            user_model_org = body.user_model_org, 
            user_model_creator_id = body.user_model_creator_id, 
            user_model_description = body.user_model_description
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        for profession in body.user_model_professions:
            post_user_profession(user.user_model_id, profession)
        
        for area in body.user_model_working_areas:
            post_user_working_area(user.user_model_id, area)

        return (Response(), 201)

    return (Response(), 401)

"""
DELETE /users

body:
UserModel
"""
@token_required
def delete_user_by_id(user_model_id): # noqa: E501
    """delete_user_by_id

    Delete user by id # noqa: E501

    :rtype: Response
    """

    # Remove professions (theirs evidences too)
    professions = DBProfession.query.filter(DBProfession.profession_user == user_model_id).all()
    for profession in professions:
        delete_profession(profession.profession_id)
    
    areas = DBWorkingArea.query.filter(DBWorkingArea.working_area_user == user_model_id).all()
    for area in areas:
        delete_working_area(area.working_area_id)

    db.session.query(DBUserModel).filter(DBUserModel.user_model_id == user_model_id).delete()
    db.session.commit()
    return (Response(), 201)

# TODO: Erase hasher
def get_hash(param): # noqa: E501
    return make_response(jsonify({'hashed': generate_password_hash(param)}), 201)





"""
-----------------------------------------------------
@author: David Lopez
@date: February 02, 2022
-----------------------------------------------------
"""

"""
GET /users/:id/professions
"""
# TODO: Check token required implementation
# @token_required
def get_user_professions(user_model_id):
    """get_user_professions

    Show a listing of user professions # noqa: E501

    :rtype: List[Profession]
    """

    professions = DBProfession.query.filter(DBProfession.profession_user == user_model_id).all()
    if professions == None:
        abort(404)
    return [Profession(
        profession_id=p.profession_id, 
        profession_skill=p.profession_skill, 
        profession_evidences=get_evidences_profession(p.profession_id)) for p in professions]

"""
GET /professions/:id/evidences
"""
# TODO: Check token required implementation
# @token_required
def get_evidences_profession(profession_id):
    """get_evidences_profession

    Show a listing of profession evidences # noqa: E501

    :rtype: List[Evidence]
    """

    evidences = DBEvidence.query.filter(DBEvidence.evidence_profession == profession_id).all()
    if evidences == None:
        abort(404)
    return [Evidence(
        evidence_id = e.evidence_id, 
        evidence_media = e.evidence_media) for e in evidences]

"""
POST /address

body:
UserAddress
"""
@token_required
def post_address(body):
    """post_address

    Create UserAddress # noqa: E501

    :rtype: UserAddress
    """

    if connexion.request.is_json:
        body = UserAddress.from_dict(connexion.request.get_json())

        address = DBUserAddress(
            street_name = body.street_name, 
            main_number = body.main_number, 
            interior_number = body.interior_number, 
            id_colony_code = body.id_colony_code, 
            id_state_code = body.id_state_code, 
            id_municipality = body.id_municipality, 
            id_country_code = body.id_country_code,  
            id_zip_code = body.id_zip_code
        )

        db.session.add(address)
        db.session.commit()
        db.session.refresh(address)

        return UserAddress(
            street_name = address.street_name, 
            main_number = address.main_number, 
            interior_number = address.interior_number, 
            id_colony_code = address.id_colony_code, 
            id_state_code = address.id_state_code, 
            id_municipality = address.id_municipality, 
            id_country_code = address.id_country_code,  
            id_zip_code = address.id_zip_code, 
            id_user_address = address.id_user_address, 
            date_added = address.date_added, 
            last_update_date = address.last_update_date)

    return (Response(), 401)

"""
PUT /users/:id/address

body:
UserAddress
"""
@token_required
def put_address(user_model_id, body): # noqa: E501
    """put_address

    Update user address # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        body = UserAddress.from_dict(connexion.request.get_json())
        
        user_address = get_user_address_by_id(user_model_id)
        if user_address is None:
            abort(404)
        
        # Only if the row exists
        db.session.query(DBUserAddress).filter(DBUserAddress.id_user_address == body.id_user_address).update(
            {DBUserAddress.id_colony_code : body.id_colony_code, 
            DBUserAddress.id_country_code : body.id_country_code, 
            DBUserAddress.id_municipality : body.id_municipality, 
            DBUserAddress.id_state_code : body.id_state_code, 
            DBUserAddress.id_zip_code : body.id_zip_code, 
            DBUserAddress.interior_number : body.interior_number, 
            DBUserAddress.main_number : body.main_number, 
            DBUserAddress.street_name : body.street_name}, synchronize_session="fetch")

        db.session.commit()
        return (Response(), 201)

    return (Response(), 401)

"""
DELETE /users/:id/address
"""
@token_required
def delete_address(user_model_id):
    """delete_address

    Delete User Address # noqa: E501

    :rtype: Response
    """

    user_model = get_user_by_id(user_model_id)
    db.session.query(DBUserAddress).filter(DBUserAddress.id_user_address == user_model.user_model_address_id).delete()
    db.session.commit()
    return (Response(), 201)




"""
-----------------------------------------------------
@author: David Lopez
@date: February 07, 2022
-----------------------------------------------------
"""

"""
POST /users/:id/professions
"""
@token_required
def post_user_profession(user_model_id, body):
    """post_user_profession

    Post user profession # noqa: E501

    :rtype: Profession
    """

    if connexion.request.is_json:
        if type(body) is not Profession:
            body = Profession.from_dict(connexion.request.get_json())

        profession = DBProfession(
            profession_skill = body.profession_skill, 
            profession_user = user_model_id
        )

        db.session.add(profession)
        db.session.commit()
        db.session.refresh(profession)

        for evidence in body.profession_evidences:
            post_profession_evidence(profession.profession_id, evidence)

        return (Response(), 201)

    return (Response(), 401)

"""
POST /professions/:id/evidences
"""
@token_required
def post_profession_evidence(profession_id, body):
    """post_profession_evidence

    Post profession evidence # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        if type(body) is not Evidence:
            body = Evidence.from_dict(connexion.request.get_json())

        evidence = DBEvidence(
            evidence_media = body.evidence_media, 
            evidence_profession = profession_id
        )

        db.session.add(evidence)
        db.session.commit()
        db.session.refresh(evidence)
        return (Response(), 201)

    return (Response(), 401)

"""
DELETE /professions/:id
"""
@token_required
def delete_profession(profession_id):
    """delete_profession

    Delete profession # noqa: E501

    :rtype: Response
    """

    # Remove evidences of this profession
    evidences = DBEvidence.query.filter(DBEvidence.evidence_profession == profession_id).all()
    for evidence in evidences:
        delete_evidence(evidence.evidence_id)

    db.session.query(DBProfession).filter(DBProfession.profession_id == profession_id).delete()
    db.session.commit()
    return (Response(), 201)

"""
DELETE /evidences/:id
"""
@token_required
def delete_evidence(evidence_id):
    """delete_evidence

    Delete evidence # noqa: E501

    :rtype: Response
    """

    # Remove media of this evidence
    evidence = DBEvidence.query.filter(DBEvidence.evidence_id == evidence_id).first()
    db.session.query(DBEvidence).filter(DBEvidence.evidence_id == evidence_id).delete()
    db.session.query(DBMedia).filter(DBMedia.media_id == evidence.evidence_media).delete()
    
    # Save changes
    db.session.commit()
    return (Response(), 201)


"""
-----------------------------------------------------
@author: David Lopez
@date: February 07, 2022
-----------------------------------------------------
"""

"""
GET /users/:id/working_areas
"""
# TODO: Check token required implementation
# @token_required
def get_user_working_areas(user_model_id):
    """get_user_working_areas

    Show a listing of user working areas # noqa: E501

    :rtype: List[WorkingArea]
    """

    areas = DBWorkingArea.query.filter(DBWorkingArea.working_area_user == user_model_id).all()
    if areas == None:
        abort(404)
    return [WorkingArea(
        working_area_id = a.working_area_id, 
        working_area_municipality = a.working_area_municipality) for a in areas]

"""
DELETE /working_areas/:id
"""
@token_required
def delete_working_area(working_area_id):
    """delete_working_area

    Delete working area # noqa: E501

    :rtype: Response
    """

    db.session.query(DBWorkingArea).filter(DBWorkingArea.working_area_id == working_area_id).delete()
    db.session.commit()
    return (Response(), 201)

"""
POST /users/:id/working_areas
"""
@token_required
def post_user_working_area(user_model_id, body):
    """post_user_working_areas

    Post user working area # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        if type(body) is not WorkingArea:
            body = WorkingArea.from_dict(connexion.request.get_json())

        area = DBWorkingArea(
            working_area_municipality = body.working_area_municipality, 
            working_area_user = user_model_id
        )

        db.session.add(area)
        db.session.commit()
        db.session.refresh(area)
        return (Response(), 201)

    return (Response(), 401)

"""
-----------------------------------------------------
@author: David Lopez
@date: February 20, 2022
-----------------------------------------------------
"""

"""
GET /users/public

Token is not required
"""
def get_public_users_info():
    """get_public_users_info

    Get all public users info # noqa: E501

    :rtype: List[PublicUserModel]
    """

    USER_ROLE_PROFESSIONAL = DBUserRole.query.filter(DBUserRole.user_role_name.like('%PROFESIONAL%')).first()
    users = DBUserModel.query.filter(DBUserModel.user_role_id == USER_ROLE_PROFESSIONAL.user_role_id).all()
    if users == None:
        abort(404)

    return [PublicUserModel(
        user_model_id = u.user_model_id, 
        user_role_id = u.user_role_id, 
        user_model_first_name = u.user_model_first_name, 
        user_model_last_name = u.user_model_last_name, 
        user_model_surname = u.user_model_surname, 
        user_model_phone_number = u.user_model_phone_number, 
        user_model_media_id = u.user_model_media_id, 
        user_model_org = u.user_model_org, 
        user_model_description = u.user_model_description,
        user_model_professions = get_user_professions(u.user_model_id),
        user_model_working_areas = get_user_working_areas(u.user_model_id)
    ) for u in users]




"""
-----------------------------------------------------
@author: David Lopez
@date: May 13, 2022
-----------------------------------------------------
"""

"""
DELETE /address/:id
"""
@token_required
def delete_address_by_id(user_address_id):
    """delete_address_by_id

    Delete User Address # noqa: E501

    :rtype: Response
    """

    db.session.query(DBUserAddress).filter(DBUserAddress.id_user_address == user_address_id).delete()
    db.session.commit()
    return (Response(), 201)