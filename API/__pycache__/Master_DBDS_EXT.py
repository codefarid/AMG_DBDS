import os
from flask import Blueprint, Response, jsonify, json, request
from DB import *
from Helpers import *
from datetime import datetime
from Decorators import *

master_dbds_ext = Blueprint('master_dbds_ext',__name__)


@master_dbds_ext.route('/api/master_dbds_ext', methods=['GET', 'POST'])
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
    # #user = 'bryan.patty'
    if request.method == 'GET':
        return jsonify(0)
    if request.method == 'POST':
        # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401

        data = request.get_json()
        headerId = data['extTableName'].upper()
        date = datetime.now()
        time = date.strftime("%H%M")
        user = "santoso"
        date = date.strftime("%Y%m%d")
        isExist = '1' 
        print(data,'?/////////?')
        getName = data['extName']
        cur_sql.execute("""
                        Select AAMTBIDZ1302 as caption from AAMTBHAZ1301 where AAMTBIDZ1302 = '{ids}'
                        """.format(ids = headerId))
        
        rows = cur_sql.fetchall()
        if rows:
            return jsonify({'message':"ID already exist!"})
        else:
            appName = data['appName']['text']
            
            if len(headerId) == 8:
                getCate = headerId[4]
            if len(headerId) == 6:
                getCate = headerId[2]
            getQuery = postExtQuery(data)
            
            
            
            cur_sql.execute("""
                            Select AAMCAVAZ1302 as 'code' 
                            From AAMTCATEZ1301 where AAMCKEYZ1302 like '%{kat}%'
                            """.format(kat = getCate))
            kategori = cur_sql.fetchone()[0]
            print(kategori)
            msg = {
                    'message' : ''
             }

            # if kategori == None:
            #     return jsonify(msg)
            # else:
            cur_sql.execute("""
                            Select AMAPCA101 as 'app_id' from AAM101
                                WHERE AMAPNA101 = '{appName}'
                            """.format(appName = appName))
            results = cur_sql.fetchall()
            appId = results[0][0]
            status = "active"
            joinTo = data['joinTo']
            
              
            cur_sql.execute("""
                                INSERT INTO AAMTBHAZ1301 (AAMTBIDZ1302,AAMCPTBZ1302,AAMALIDZ1302,AAMALNMZ1302,AAMKTAPZ1302,AAMQESRZ1302,AAMTHSTZ1302,AAMJOINZ1302,AAMEXTTZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302)
                                values 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                """,(headerId, getName, appId, appName,kategori, getQuery ,status,joinTo, isExist, date, time, user, date, time, user))
                

                    
            for el in data['field']:
                    print(el['extFname'],'/.,./,///////////')
                    fieldName = ''
                    if el['extFname']:
                        fieldName = el['extFname']
                    else :
                        fieldName = el['extFname']['key']
                    fieldId = el['fieldName'].upper()
                    daType = el['datTypeField'].upper()
                    maxVal = el['maxlenField']
                    isPk = '1' if el['isPk'] else '0'
                    
                        
                    cur_sql.execute("""
                                    INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302,AAMSTTDZ1301)
                                    values (%s , %s , %s , %s , %s ,%s, %s , %s , %s , %s , %s, %s,%s,%s);
                                    """,(fieldId,headerId,fieldName,maxVal,daType,isPk,isExist ,date, time, user, date, time, user,status))
                    
                    # code = fieldId[0:4].upper()

                    # cur_sql.execute("""
                    #                 select
                    #                     AAMTBCOZ1302 as 'code',
                    #                     AAMTDEFZ1302 as 'value',
                    #                     AAMDSTAZ1302 as 'status'
                    #                     from AAMTBDEZ1301 
                    #                     where AAMTBCOZ1302 = '{code}'
                    #                 """.format(code = code))
                    # detectCode = cur_sql.fetchone()

                    # msg = {
                    #     'message' : 'Belum mendaftarkan Field di dictionary, silahkan daftarkan dulu!'
                    # }

                    # if detectCode != None:
            msg['message'] = 'Sukes menambahkan Tabel!'
                    #     DB_SQL.commit()
                    #     return jsonify(msg)
                    # else:
                    #     return jsonify(msg)
            DB_SQL.commit()
        return jsonify(msg)
    
    
@master_dbds_ext.route('/api/master_dbds_ext/<string:id>', methods=["GET",'PUT'])
def putExtTable(id):
        # token = request.headers['Authorization']
    # appCode = decrypt_text(request.headers['App'].encode())
    # auth_page = check_user_auth_page(token, appCode, 4)
    # if not auth_page:
    #     return jsonify({'message': 'Token Invalid'}), 403
    # else:
    #     auth_page = auth_page.get_json()
    #     auth_page = list(auth_page)
    # user = check_user(token, amg = True)
    
    date = datetime.now()
    time = date.strftime("%H%M")
    date = date.strftime("%Y%m%d")
    user = 'santoso'
    
    if request.method == 'GET':
        # if auth_page[0] != '1':
        #         return jsonify({'message': 'Not Authorized'}), 401
        
        cur_sql.execute("""
            SELECT
                AAMTBIDZ1302 as table_id ,
                AAMCPTBZ1302 as caption_table,
                AAMALIDZ1302 as aplication_id,
                AAMALNMZ1302 as aplication_name,        
                AAMKTAPZ1302 as kategori_app,
                AAMQESRZ1302 as query_string,
                AAMJOINZ1302 as joinTo ,
                AAMEXTTZ1301 as isExist 
            from AAMTBHAZ1301
            where AAMTBIDZ1302 = %s
            """, (id,))
        result1 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]

        
        cur_sql.execute("""
            SELECT 
                AAMFEIDZ1302 as field_id,
                AAMHAIDZ1302 as header_id,
                AAMNMZ1302 as name_caption,
                AAMVLZ1302 as default_value,
                AAMDTZ1302 as data_type,
                AAMPKZ1302 as statPk,
                AAMEXTDZ1301 as isExistField,
                AAMSTTDZ1301 as 'statTD'
            FROM AAMTBDTZ1301
            where AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
            """,(id,))
        result2 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]

        result_dict = {'table_data': result1, 'field_data': result2}
    
        return jsonify(result_dict)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        headerId = id
        date = datetime.now()
        time = date.strftime("%H%M")
        user = "santoso"
        date = date.strftime("%Y%m%d")
        appName = data['appName']['text']
        kategori = data['isMaster']['value']
        isExist = '1' 
        
        cur_sql.execute("""
                            Select AMAPCA101 as 'app_id' from AAM101
                                WHERE AMAPNA101 = '{appName}'
                            """.format(appName = appName))
        results = cur_sql.fetchall()
        appId = results[0][0]
        
        editedQuery = editExtQuery(data, headerId)
        
        filteredObj = recreateObj(data)
        newCreatedQuery = postExtQuery(filteredObj)
        
        
        cur_sql.execute("""
                UPDATE AAMTBHAZ1301
                SET
                    AAMCPTBZ1302 = %s,
                    AAMALIDZ1302 = %s,
                    AAMALNMZ1302 = %s,        
                    AAMKTAPZ1302 = %s,
                    AAMQESRZ1302 = %s,
                    AAMTHISZ1301 = %s,
                    AAMUDATZ1302 = %s,
                    AAMUDTMZ1302 = %s,
                    AAMUDUEZ1302 = %s
                WHERE
                    AAMTBIDZ1302 = %s
                """,(data['tableName'], appId, appName, kategori, newCreatedQuery, editedQuery, date, time, user,headerId))
        
        DB_SQL.commit()
        
        cur_sql.execute("""
            SELECT 
                AAMFEIDZ1302 as field_id,
                AAMHAIDZ1302 as header_id,
                AAMNMZ1302 as name_caption,
                AAMVLZ1302 as default_value,
                AAMDTZ1302 as data_type,
                AAMPKZ1302 as statPk,
                AAMSTTDZ1301 as 'statTD'
            FROM AAMTBDTZ1301
            where AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
            """,(id,))
        oldDatas = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        oldLen = len(oldDatas)
        newLen = len(data['field'])
        
        if oldLen != newLen:
            newFields = data['field'][oldLen: newLen]
            print(newFields,"?EXT???????")
            if oldLen < newLen:
                for y in newFields:
                    if y['extFname']:
                        fieldName =  y['extFname']
                    else:
                        fieldName = y['extFname']['key']
                    newIds = y['fieldName'].upper()
                    newDat = y['datTypeField'].upper()
                    newMaxVal = y['maxlenField']
                    stat = 'active'
                    
                    isPk = '1' if y['isPk'] else '0'
                    
                    cur_sql.execute("""
                                    INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302, AAMSTTDZ1301)
                                    values (%s , %s , %s , %s , %s , %s , %s , %s , %s ,%s, %s, %s,%s, %s);
                                    """,(newIds,headerId,fieldName,newMaxVal,newDat,isPk,isExist,date, time, user, date, time, user,stat))
                    DB_SQL.commit()
            else:
                #  removedField = old['field_data'][len(inputNew['field']):len(old['field_data'])]
                removeField = oldDatas[newLen : oldLen]
                for x in removeField:
                    removedId = x['field_id']
                    cur_sql.execute("""
                                    UPDATE AAMTBDTZ1301
                                    SET 
                                        AAMSTTDZ1301 = 'inactive'
                                    WHERE 
                                        AAMFEIDZ1302 = '{ids}'
                                    """.format(ids=removedId))
                    DB_SQL.commit()
                    
                print(removeField,'?? PUT REMOVE FIELD EXT TABLE')
                    
                
        else:
            for el in data['field']:
                print(el,"<><><><><><EXT><><>?")
                fieldName = ''
                fieldId = ''
                if el['extFname']['key']:
                    fieldName = el['extFname']['key']
                else:
                    fieldName = el['fieldName']['key']
                    
                if el['fieldName']['value']:
                    fieldId = el['fieldName']['value'].upper()
                else:
                    fieldId = el['fieldName'].upper()
                # fieldId = generateIdTDetail(y['fieldNameEdit']['value'], id)
                # fieldName = el['fieldNameEdit']['key']
                    
                daType = el['datTypeField'].upper()
                maxlen = el['maxlenField']
                isPk = '1' if el['isPk'] else '0'
                statTD = el['statTD']
                
                cur_sql.execute("""
                            UPDATE AAMTBDTZ1301
                            SET
                                AAMHAIDZ1302 = %s,
                                AAMNMZ1302 = %s,        
                                AAMVLZ1302 = %s,
                                AAMDTZ1302 = %s,
                                AAMPKZ1302 = %s,
                                AAMEXTDZ1301 = %s,
                                AAMSTTDZ1301 = %s,
                                AAMUDATZ1302 = %s,
                                AAMUDTMZ1302 = %s,
                                AAMUDUEZ1302 = %s
                            WHERE
                                AAMFEIDZ1302 = %s
                            """,(headerId,fieldName,maxlen,daType,isPk,isExist,statTD,date, time, user,fieldId))
                DB_SQL.commit()
 
        return jsonify(0)