import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json

query_generator = Blueprint('query_generator',__name__)
module_id = 1
        
@query_generator.route('/api/query_generator', methods=['GET','POST'])
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
                        TBDEM1501 as 'key',
                        STATM1501 as 'status' 
                        FROM AAM1501 where STATM1501 = 'active' or STATM1501 = 'on'
                        """) 
        
        sugestionField = []
        for row in cur_sql:
                    sugestionField.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        
        cur_sql.execute("""
                        SELECT 
                            CANOM1601 as 'value',
                            CANAM1601 as 'key',
                            STATM1601 as 'status'
                        FROM AAM1601 where STATM1601 = 'active'
                        """)
        category = []
        for row in cur_sql:
                    category.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
          
        cur_sql.execute("""
                        Select 
                            TBIDM1701 as 'value' ,
                            CPTBM1701 as 'text',
                            APNAM1701 as 'app'
                        From AAM1701
                            Where STATM1701 = 'active'
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
    
@query_generator.route('/api/query_generator/getFkeyData',methods=['GET'])
def sendData():
    cur_sql.execute("""
                SELECT    
                AAM1701.TBIDM1701 AS table_id,
                AAM1701.CPTBM1701 AS caption_table,
                AAM1701.APNAM1701 AS aplication_name,
                AAM1801.FEIDM1801 AS field_id,
                AAM1801.NMCAM1801 AS name_caption
                FROM
                AAM1701
                INNER JOIN 
                AAM1801 ON AAM1701.TBIDM1701 = AAM1801.AAMHAIDZ1302
                where STATM1701 = 'active';
                """)
    rawData = []
    for row in cur_sql:
        rawData.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
    counter = 0
    counter2= 0
    dataSB = []
    for el in rawData:
        existingItem = next((item for item in dataSB if item["data"] == el["table_id"] and item["label"] == el["caption_table"]), None)
        # print(existingItem)
        if existingItem:
            counter2 += 1
            secNum = int(existingItem["children"][-1]["key"].split("-")[1])
            existingItem['children'].append({
                        "key": f'{existingItem["key"]}-{secNum + 1}',
                        "label": el['name_caption'],
                        "data": el['field_id'],
                        "icon": 'pi pi-fw pi-server'
                    })
        else:
            counter2 += 1
            dataSB.append({
                "key": f'{counter}',
                "label": el['caption_table'],
                "data": el['table_id'],
                "icon": 'pi pi-fw pi-table',
                "app": el['aplication_name'],
                "children": [{
                        "key": f'{counter}-{0}',
                        "label": el['name_caption'],
                        "data": el['field_id'],
                        "icon": 'pi pi-fw pi-server'
                    }]})
            # counter2 = 0
        counter += 1
        counter2 = 0

    return jsonify({"data": dataSB})

