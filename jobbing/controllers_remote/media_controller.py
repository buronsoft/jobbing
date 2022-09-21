"""
-----------------------------------------------------
@author: David Lopez
@date: February 02, 2022
-----------------------------------------------------
"""

import base64

from flask import abort, Response, make_response
import connexion
from jobbing.db import db

from jobbing.login import token_required

from jobbing.DBModelsRemote import Media as DBMedia
from jobbing.models_remote.media import Media # noqa: E501

"""
GET /media/:id
"""
def get_media_by_id(media_id):
    """get_media_by_id

    Get Media by id

    :rtype: Media
    """

    media = DBMedia.query.filter(DBMedia.media_id == media_id).first()
    if media == None:
        abort(404)

    return Media(
        media_status_id = media.media_status_id, 
        media_data = media.media_data.decode(), 
        media_link = media.media_link, 
        media_title = media.media_title, 
        media_description = media.media_description, 
        media_size = media.media_size, 
        media_id = media.media_id, 
        media_content_upload_date = media.media_content_upload_date, 
        media_content_updated_date = media.media_content_updated_date)

"""
POST /media

body:
Media
"""
@token_required
def post_media(body):
    """post_media

    Create new media content #noqa: E501

    :rtype: Media
    """

    if connexion.request.is_json:
        body = Media.from_dict(connexion.request.get_json())

        media = DBMedia(
            media_status_id = body.media_status_id, 
            media_data = bytes(body.media_data, 'utf-8'), 
            media_link = body.media_link, 
            media_title = body.media_title, 
            media_description = body.media_description, 
            media_size = body.media_size
        )

        db.session.add(media)
        db.session.commit()
        db.session.refresh(media)

        return Media(
            media_status_id = media.media_status_id, 
            media_data = media.media_data.decode(), 
            media_link = media.media_link, 
            media_title = media.media_title, 
            media_description = media.media_description, 
            media_size = media.media_size, 
            media_id = media.media_id, 
            media_content_upload_date = media.media_content_upload_date, 
            media_content_updated_date = media.media_content_updated_date)
        
    return (Response(), 401)

"""
PUT /media

body:
Media
"""
@token_required
def put_media(body): # noqa: E501
    """put_media

    Update media # noqa: E501

    :rtype: Response
    """

    if connexion.request.is_json:
        body = Media.from_dict(connexion.request.get_json())
        
        media = get_media_by_id(body.media_id)
        if media is None:
            abort(404)
        
        # Only if the row exists
        db.session.query(DBMedia).filter(DBMedia.media_id == body.media_id).update(
            {DBMedia.media_data : bytes(body.media_data, 'utf-8'), 
            DBMedia.media_description : body.media_description, 
            DBMedia.media_link : body.media_link, 
            DBMedia.media_size : body.media_size, 
            DBMedia.media_status_id : body.media_status_id, 
            DBMedia.media_title : body.media_title}, synchronize_session="fetch")

        db.session.commit()
        return (Response(), 201)

    return (Response(), 401)

"""
DELETE /media/:id
"""
@token_required
def delete_media_by_id(media_id):
    """delete_media

    Delete media # noqa: E501

    :rtype: Response
    """

    db.session.query(DBMedia).filter(DBMedia.media_id == media_id).delete()
    db.session.commit()
    return (Response(), 201)

"""
-----------------------------------------------------
@author: David Lopez
@date: February 20, 2022
-----------------------------------------------------
"""

"""
GET /media/:id/content

Token is not required
"""
def get_media_content_by_id(media_id):
    """get_media_content_by_id

    Get Media Content by id

    :rtype: HttpResponse (img tag)
    """

    media = DBMedia.query.filter(DBMedia.media_id == media_id).first()
    if media == None:
        abort(404)

    return Response(base64.b64decode(media.media_data.decode()), mimetype='image/jpeg')