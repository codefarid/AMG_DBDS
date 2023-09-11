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
                        select AAMCAVAZ1302 as code , AAMCKEYZ1302 as label, AAMDACAZ1302 as 'created', AAMUSCAZ1302 as 'user', AAMCSTAZ1302 as status from AAMTCATEZ1301
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
                                Select TOP 1 AAMCAVAZ1302 as 'value' from AAMTCATEZ1301 order by AAMCAVAZ1302 DESC
                                """)
        categories = cur_sql.fetchone()
        if categories:
            newVal = str(int(categories[0]) + 1)
        else :
            newVal = str(1)
        
        cur_sql.execute("""
                                Select AAMCKEYZ1302 as code from AAMTCATEZ1301 where AAMCKEYZ1302 like '%{names}%'
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
                                INSERT INTO AAMTCATEZ1301( AAMCAVAZ1302, AAMCKEYZ1302, AAMDACAZ1302, AAMTACAZ1302, AAMUSCAZ1302, AAMUDACZ1302,  AAMUTACZ1302, AAMUUSCZ1302, AAMCSTAZ1302)
                                VALUES (%s, %s, %s ,%s ,%s, %s ,%s ,%s, %s)
                                """,(newVal, category,date,time,user,date,time,user, status))
            DB_SQL.commit()
            return jsonify(0)

@master_categories.route('/api/master_categories/<string:id>', methods=['GET','PUT'])
def putCate(id):
    if request.method == "GET":
        cur_sql.execute("""
                        select AAMCKEYZ1302 as label, AAMCSTAZ1302 as status from AAMTCATEZ1301
                        where AAMCAVAZ1302 = %s
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
        #                         Select AAMCKEYZ1302 as code from AAMTCATEZ1301 where AAMCKEYZ1302 = '{names}'
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
                            UPDATE AAMTCATEZ1301
                            SET
                                AAMCKEYZ1302 = %s,
                                AAMUDACZ1302 = %s,
                                AAMUTACZ1302 = %s,
                                AAMUUSCZ1302 = %s,
                                AAMCSTAZ1302= %s
                            WHERE AAMCAVAZ1302 = %s
                            """,(category,date,time,user,status, id))
        DB_SQL.commit()
            
        return jsonify(0)
        
        