import os
from flask import Blueprint, Response, jsonify, json, request
from DB import *
from datetime import datetime
from Decorators import *
import decimal
import pandas as pd
import sys

if deploy_local:
    if test:
        sys.path.append('C:\API_APPS\Home\API_Test')
    else:
        sys.path.append('C:\API_APPS\Home\API')

if development:
    sys.path.append('D:\AMINION\menu-dms')

from Menu import *

master_menu = Blueprint('master_menu',__name__)

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


master_menu.json_encoder = MyJSONEncoder

@master_menu.route('/api/master_menu', methods=['GET'])
@check_for_token
def index():
    if request.method == 'GET':
        appCode = decrypt_text(request.headers['App'].encode())
        user = check_user(request.headers['Authorization'], amg = True)
        menus = menu(user, appCode)
        print(menus)
        return menus

@master_menu.route('/api/master_menu/auth/<string:menuCode>', methods=['GET'])
@check_for_token
def authPage(menuCode):
    if request.method == 'GET':
        appCode = decrypt_text(request.headers['App'].encode())
        user = check_user(request.headers['Authorization'], amg = True)
        return auth_page(user, appCode, menuCode)
