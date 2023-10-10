import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json


master_dictionaries = Blueprint('master_dictionaries',__name__)
module_id = 3

def checkColumn(alias):
    match alias:
        case 'code':
            return 'TBNOM1501'
        case 'value':
            return 'TBDEM1501'
        case 'user':
            return 'CRUSM1501'
        case 'status':
            return 'STATM1501'
        
    return 'TBNOM1501'
        
@master_dictionaries.route('/api/master_dictionaries', methods=['GET','POST'])
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
        param = request.args.to_dict()
        
        where = ''
        
        if param['globalFilter'] != 'null':
            where = '''WHERE TBNOM1501 like '%{filter}%' OR
                            TBDEM1501 like '%{filter}%' OR
                            CRUSM1501 like '%{filter}%' OR
                            STATM1501 like '%{filter}%'
                    '''.format(filter = param['globalFilter'])
        cur_sql.execute("""
                        Select 
                            COUNT(*) as totalData
                        From AAM1501 {where}
                        """.format(where = where))
        
        totalData = cur_sql.fetchone()[0]
        orderByCol = checkColumn(param['orderBy'])
        orderByMethod = param['orderMethod']
        
        
        
        cur_sql.execute("""
                        SELECT 
                            TBNOM1501 as code, 
                            TBDEM1501 as value, 
                            CRUSM1501 as 'user', 
                            STATM1501 as 'status' 
                        FROM AAM1501 {where}
                        ORDER BY {col} {method}
                        OFFSET {before} ROWS
                        FETCH NEXT {totalData} ROWS ONLY;
                        """.format(
                            where = where,
                            col = orderByCol, 
                            method = orderByMethod, 
                            before = int(param['dataBefore']), 
                            totalData = int(param['dataBefore'])+int(param['dataPerPage'])
                        )) 
        
        results = []
        for row in cur_sql:
            results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

        for item in results:
            item['status'] = 'active' if item['status'] == 'on' else item['status']
            
        data = {
            "totalRecord": totalData,
            "result": results
        }
        return jsonify(data)
    if request.method == 'POST':
        # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401

        data = request.get_json()
        
        getCode = data['code'].upper()
        code = getCode[1:5]
        value = data['value']
        status = "active"
        
        date = datetime.now()
        time = date.strftime("%H%M")
        date = date.strftime("%Y%m%d")
        # user = 'santoso'
        
        
        cur_sql.execute("""
                                Select TBDEM1501 as caption from AAM1501 where TBDEM1501 = '{names}'
                                """.format(names =  value))
        rows = cur_sql.fetchone()        
        
        if rows:
            if value.upper() == rows[0].upper():
                return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
            duplicated_name = rows[0]
        else:
            duplicated_name = [''] 
            
               
        if len(duplicated_name) > 0 and value in duplicated_name:
            return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
        else:
            cur_sql.execute("""
                                            INSERT INTO AAM1501 (TBNOM1501 , TBDEM1501, CRDTM1501, CRTMM1501, CRUSM1501, UPDTM1501, UPTIM1501, UPUSM1501,STATM1501)
                                            VALUES ( %s, %s, %s ,%s ,%s, %s, %s ,%s ,%s)
                                            """, (code, value, date, time, user, date, time, user, status))
            DB_SQL.commit()
            return jsonify(0)
              
        

@master_dictionaries.route('/api/master_dictionaries/<string:id>', methods=['GET','PUT'])
def editDict(id):
    token = request.headers['Authorization']
    appCode = decrypt_text(request.headers['App'].encode())
    auth_page = check_user_auth_page(token, appCode, module_id)
    if not auth_page:
        return jsonify({'message': 'Token Invalid'}), 403
    else:
        auth_page = auth_page.get_json()
        auth_page = list(auth_page)
    user = check_user(token, amg = True)
    if request.method == "GET":
        cur_sql.execute("""
                        select 
                            TBNOM1501 as 'code', 
                            TBDEM1501 as 'value', 
                            STATM1501 as 'status' 
                        from AAM1501
                        where TBNOM1501 = %s
                        """, (id,))
        results = []
        for row in cur_sql:
            results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        data = {
            "result" : results
        }
     
        return jsonify(data)
    if request.method == "PUT":
        # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401

        data = request.get_json()
        
        getCode = data['code']
        code = getCode[0:5]
        value = data['value']
        status = data['stat']
        
        date = datetime.now()
        time = date.strftime("%H%M")
        date = date.strftime("%Y%m%d")

        # user = 'santoso'
        
        cur_sql.execute("""
                                Select TBDEM1501 as caption from AAM1501 where TBDEM1501 = '{names}'
                                """.format(names =  value))
        rows = cur_sql.fetchone()
        
        
        # if rows:
        #     if value.upper() == rows[0].upper():
        #         return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
        #     duplicated_name = rows[0]
        # else:
        #     duplicated_name = ['']       
        # if len(duplicated_name) > 0 and value in duplicated_name:
        #     return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
        # else:
        cur_sql.execute("""
                            UPDATE AAM1501
                            SET
                                TBDEM1501 = %s,
                                AAMUDDEZ1302 = %s,
                                AAMUTDEZ1302 = %s,
                                AAMUUDEZ1302 = %s,
                                STATM1501= %s
                            WHERE TBNOM1501 = %s
                            """, ( value, date, time, user, status,code))
        DB_SQL.commit()
              
        
        return jsonify(0)