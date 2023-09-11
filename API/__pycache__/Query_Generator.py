import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json

query_generator = Blueprint('query_generator',__name__)

        
@query_generator.route('/api/query_generator', methods=['GET','POST'])
# @check_for_token
def index():
    # token = request.headers['Authorization']
    # appCode = decrypt_text(request.headers['App'].encode())
    # auth_page = check_user_auth_page(token, appCode, 4)
    # if not auth_page:
    #     return jsonify({'message': 'Token Invalid'}), 403
    # else:
    #     auth_page = auth_page.get_json()
    #     auth_page = list(auth_page)
    # user = check_user(token, amg = True)
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
                        AAMTBCOZ1302 as 'value',
                        AAMTDEFZ1302 as 'key',
                        AAMDSTAZ1302 as 'status' 
                        FROM AAMTBDEZ1301 where AAMDSTAZ1302 = 'active' 
                        """) 
        
        sugestionField = []
        for row in cur_sql:
                    sugestionField.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        cur_sql.execute("""
                        SELECT 
                            AAMCAVAZ1302 as 'value',
                            AAMCKEYZ1302 as 'key',
                            AAMCSTAZ1302 as status
                        FROM AAMTCATEZ1301 where AAMCSTAZ1302 = 'active'
                        """)
        category = []
        for row in cur_sql:
                    category.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
          
        cur_sql.execute("""
                        Select 
                            AAMTBIDZ1302 as 'value' ,
                            AAMCPTBZ1302 as 'text',
                            AAMALNMZ1302 as 'app'
                        From AAMTBHAZ1301
                            Where AAMTHSTZ1302 = 'active'
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
        getQuery = postQuery(data)
        return jsonify(getQuery)
    
    
@query_generator.route('/api/query_generator/<string:id>', methods=["GET",'PUT'])
def appendQuery(id):
    if request.method == 'GET':
        msg = { "msg": "WAIT!"}
        return jsonify(msg)
    if request.method == 'PUT':
        result = ''
        data = request.get_json()
        print(data)
        if data['isExisted'] == '1':
            print("GENERATING EDITED EXISTING TABLE")
            result = editExtQuery(data,id)
        else:
            print("GENERATING EDITED TABLE")
            result = editQuery(data,id)
        res = {
            "queries": result
        }
        return jsonify(res)
    



