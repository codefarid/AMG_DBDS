import os
from flask import Blueprint, jsonify, request
from DB import *
from datetime import datetime
from Decorators import *
from Helpers import *
import json


master_categories = Blueprint('master_categories',__name__)

        
@master_categories.route('/api/master_categories', methods=['GET','POST'])
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
                        select
                        CANOM1601 as code ,
                        CANAM1601 as label,
                        CRDTM1601 as 'created',
                        CRUSM1601 as 'user', 
                        STATM1601 as status 
                        from AAM1601
                        """)
        results = []
        for row in cur_sql:
            results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        data = {
            "result" : results
        }
     
        return jsonify(data)
    if request.method == 'POST':
        data = request.get_json()
        date = datetime.now()
        time = date.strftime("%H%M")
        date = date.strftime("%Y%m%d")
        user = 'santoso'
        category = data['ctText']
        status = "active"
        
        cur_sql.execute("""
                                Select TOP 1 
                                CANOM1601 as 'value' 
                                from AAM1601
                                order by CANOM1601 DESC
                                """)
        categories = cur_sql.fetchone()
        if categories:
            newVal = str(int(categories[0]) + 1)
        else :
            newVal = str(1)
        
        cur_sql.execute("""
                                Select 
                                CANOM1601 as code 
                                from 
                                AAM1601 
                                where CANOM1601 like '%{names}%'
                                """.format(names =  category))
        rows = cur_sql.fetchone()
        
        if rows:
            duplicated_name = rows[0]
            if category.upper() == duplicated_name.upper():
                return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
            print(duplicated_name, category)
        else:
            duplicated_name = ['']       
                   
            cur_sql.execute("""
                                INSERT INTO AAM1601( CANAM1601, CANOM1601, CRDTM1601, CRTMM1601, CRUSM1601, UPDTM1601,  UPTIM1601, UPUSM1601, STATM1601)
                                VALUES (%s, %s, %s ,%s ,%s, %s ,%s ,%s, %s)
                                """,(newVal, category,date,time,user,date,time,user, status))
            DB_SQL.commit()
            return jsonify(0)

@master_categories.route('/api/master_categories/<string:id>', methods=['GET','PUT'])
def putCate(id):
    if request.method == "GET":
        cur_sql.execute("""
                        select CANOM1601 as label, STATM1601 as status from AAM1601
                        where CANAM1601 = %s
                        """, (id,))
        results = []
        for row in cur_sql:
            results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        data = {
            "result" : results
        }
     
        return jsonify(data)
    if request.method == "PUT":
        data = request.get_json()
        date = datetime.now()
        time = date.strftime("%H%M")
        date = date.strftime("%Y%m%d")
        user = 'santoso'
        category = data['ctText']
        status = data['stCate']
        
        # cur_sql.execute("""
        #                         Select CANOM1601 as code from AAM1601 where CANOM1601 = '{names}'
        #                         """.format(names =  category))
        # rows = cur_sql.fetchone()
        
        # if rows:
        #     duplicated_name = rows[0]
        # else:
        #     duplicated_name = ['']    
               
        # if len(duplicated_name) > 0 and category in duplicated_name:
        #     return jsonify({'message':"Nama Sudah Ada, Buat Nama lain!"})
        # else:
        cur_sql.execute("""
                            UPDATE AAM1601
                            SET
                                CANOM1601 = %s,
                                UPDTM1601 = %s,
                                UPTIM1601 = %s,
                                UPUSM1601 = %s,
                                STATM1601= %s
                            WHERE CANAM1601 = %s
                            """,(category,date,time,user,status, id))
        DB_SQL.commit()
            
        return jsonify(0)
        
        