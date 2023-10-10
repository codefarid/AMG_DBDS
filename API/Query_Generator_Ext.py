import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json

query_generator_ext = Blueprint('query_generator_ext',__name__)
module_id = 1

@query_generator_ext.route('/api/query_generator_ext', methods=["GET",'POST'])
# @check_for_token
def index():
    token = request.headers['Authorization']
    appCode = decrypt_text(request.headers['App'].encode())
    auth_page = check_user_auth_page(token, appCode, module_id)
    if not auth_page:
        return jsonify({'message': 'Token Invalid'}), 403
    else:
        auth_page = auth_page.get_json()
        auth_page = list(auth_page)
    user = check_user(token, amg = True)
    if request.method == 'GET':
        cur_sql.execute("""
                        SELECT AMAPSH101 as 'value', AMAPNA101 as 'text' from AAM101
                        WHERE AMAPCA101 <> 'Trial' AND AMAPSH101 <> 'NULL'
                        """)
        dropDownApp = []
        for row in cur_sql:
            dropDownApp.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        cur_sql.execute("""
                        SELECT
                        TBNOM1501 as 'value',
                        TBDEM1501 as 'key'
                        FROM AAM1501
                        """) 
        
        sugestionField = []
        for row in cur_sql:
                    sugestionField.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        cur_sql.execute("""
                        SELECT 
                            CANOM1601 as 'value',
                            CANAM1601 as 'key'
                        FROM AAM1601
                        """)
        category = []
        for row in cur_sql:
                    category.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
                    
        cur_sql.execute("""
                        Select 
                            TBIDM1701 as 'value' ,
                            CPTBM1701 as 'text'
                        FROM AAM1701
                        where STATM1701 = 'active'
                        """)
        joinTo = []
        for row in cur_sql:
                    joinTo.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        
        data = {
            "sugestion": sugestionField,
            "dropApp": dropDownApp,
            "category": category,
            "joinTo":joinTo
        }
        
        
        return jsonify(data)
    
    if request.method == 'POST':
        data = request.get_json()
        getQuery = postExtQuery(data)
        return jsonify(getQuery)