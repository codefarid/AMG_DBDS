import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json

master_definition = Blueprint('master_definition',__name__)

        
@master_definition.route('/api/master_definition', methods=['GET','POST'])
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
                        Select 
                            AAMTBIDZ1302 as headerId ,
                            AAMCPTBZ1302 as tableName,
                            AAMALNMZ1302 as app,
                            AAMKTAPZ1302 as categories
                            from AAMTBHAZ1301 where AAMTHSTZ1302 = 'active'
                        """)
        selectTable = []
        for row in cur_sql:
            selectTable.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        data = {
            "tables" : selectTable,
            "app": dropDownApp
        }
        
        return jsonify(data)
    
    if request.method == 'POST':
       data = request.get_json()
       
       date = datetime.now()
       time = date.strftime("%H%M")
       date = date.strftime("%Y%m%d")
       user = 'santoso'
       return jsonify(0)
       
@master_definition.route('/api/master_definition/<string:id>', methods=['GET','POST'])
def getDetailTable(id):
     if request.method == 'GET':
        cur_sql.execute("""
                       SELECT 
                            AAMFEIDZ1302 as fieldId ,
                            AAMNMZ1302 as fieldName,
                            AAMVLZ1302 as maxLen,
                            AAMDTZ1302 as datType,
                            AAMPKZ1302 as isPk 
                        FROM AAMTBDTZ1301 WHERE AAMHAIDZ1302 = %s
                        """, (id))
        data = []
        for row in cur_sql:
            data.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        data = {
            "fields" : data
        }
        
        return jsonify(data)
       
        
    
  