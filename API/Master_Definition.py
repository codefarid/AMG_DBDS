import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json

master_definition = Blueprint('master_definition',__name__)
module_id = 2
        
@master_definition.route('/api/master_definition', methods=['GET','POST'])
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
                        Select 
                            TBIDM1701 as headerId ,
                            CPTBM1701 as tableName,
                            APNAM1701 as app,
                            KTAPM1701 as categories
                            from AAM1701 where STATM1701 = 'active'
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
    #    user = 'santoso'
       return jsonify(0)
       
@master_definition.route('/api/master_definition/<string:id>', methods=['GET','POST'])
def getDetailTable(id):
     if request.method == 'GET':
        cur_sql.execute("""
                       SELECT 
                            FEIDM1801 as fieldId ,
                            NMCAM1801 as fieldName,
                            DEVAM1801 as maxLen,
                            DATYM1801 as datType,
                            ISPKM1801 as isPk 
                        FROM AAM1801 WHERE HEIDM1801 = %s
                        """, (id))
        data = []
        for row in cur_sql:
            data.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        data = {
            "fields" : data
        }
        
        return jsonify(data)
       
        
    
  