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
                        AAMTBCOZ1302 as 'value',
                        AAMTDEFZ1302 as 'key',
                        AAMDSTAZ1302 as 'status' 
                        FROM AAMTBDEZ1301 where AAMDSTAZ1302 = 'active' or AAMDSTAZ1302 = 'on'
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
        # print(data,'>>>> ')
        getQuery = postQuery(data)
        # print(getQuery)
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
                AAMTBHAZ1301.AAMTBIDZ1302 AS table_id,
                AAMTBHAZ1301.AAMCPTBZ1302 AS caption_table,
                AAMTBHAZ1301.AAMALNMZ1302 AS aplication_name,
                AAMTBDTZ1301.AAMFEIDZ1302 AS field_id,
                AAMTBDTZ1301.AAMNMZ1302 AS name_caption
                FROM
                AAMTBHAZ1301
                INNER JOIN 
                AAMTBDTZ1301 ON AAMTBHAZ1301.AAMTBIDZ1302 = AAMTBDTZ1301.AAMHAIDZ1302
                where AAMTHSTZ1302 = 'active';
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

