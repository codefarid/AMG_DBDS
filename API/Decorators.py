import json
from flask import jsonify, request, current_app
from functools import wraps
import jwt
from sqlalchemy import true
from cryptography.fernet import Fernet
from DB import *
import sys

if deploy_local:
    if test:
        sys.path.append('C:\API_APPS\Home\API_Test')
    else:
        sys.path.append('C:\API_APPS\Home\API')

if development:
    sys.path.append('D:\AMINION\menu-dms')
from Menu import *

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Missing Token'}), 403
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        
        return func(*args, **kwargs)
    return wrapped

def check_user(token, amg = False):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        if not amg:
            return data['user']
        else:
            return data['usw']
    except:
        pass

def check_user_auth_page(token, appCode, menuCode):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return auth_page(data['user'], appCode, menuCode)
    except:
        return jsonify('0000')

def check_location(user):
    cur_sql.execute("""
                    Select AMBRNO501
                    From AAM501
                    Where 
                        AMUSNO501 = '{user}'
                    """.format(
                        user = user
                    )
                )
    return cur_sql.fetchone()[0]

def encrypt_text(text):
    fernet = Fernet(current_app.config['APP_KEY'])
    return fernet.encrypt(text.encode())

def decrypt_text(text):
    fernet = Fernet(current_app.config['APP_KEY'])
    return fernet.decrypt(text).decode()