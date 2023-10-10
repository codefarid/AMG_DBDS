import os
from flask import Blueprint, Response, jsonify, json, request
from DB import *
from Helpers import *
from datetime import datetime
from Decorators import *

master_dbds_ext = Blueprint('master_dbds_ext',__name__)
module_id = 1

@master_dbds_ext.route('/api/master_dbds_ext', methods=['GET', 'POST'])
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
        return jsonify(0)
    if request.method == 'POST':
        # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401

        data = request.get_json()
        headerId = data['extTableName'].upper()
        date = datetime.now()
        time = date.strftime("%H%M")
        date = date.strftime("%Y%m%d")
        isExist = '1' 
        getName = data['extName']
        
        cur_sql.execute("""
                        Select TBIDM1701 as caption from AAM1701 where TBIDM1701 = '{ids}'
                        """.format(ids = headerId))
        
        rows = cur_sql.fetchall()
        if rows:
            return jsonify({'message':"ID already exist!"})
        else:
            appName = data['appName']['text']
            
            # if len(headerId) == 8:
            #     getCate = headerId[4]
            # if len(headerId) == 6:
            #     getCate = headerId[2]
            def getAlpha(s):
                return ''.join(filter(str.isalpha,s))

            print(getAlpha("EXIMT901")[-1])
            
            getCate = getAlpha(headerId)[-1]
            getQuery = postExtQuery(data)
            
            
            
            cur_sql.execute("""
                            Select CANOM1601 as 'code' 
                            From AAM1601 where CANAM1601 like '%{kat}%'
                            """.format(kat = getCate))
            kategori = cur_sql.fetchone()[0]
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
                                INSERT INTO AAM1701 (TBIDM1701,CPTBM1701,APNOM1701,APNAM1701,KTAPM1701,QESRM1701,STATM1701,JOINM1701,EXTTM1701,CRDTM1701,CRTMM1701,CRUSM1701,UPDTM1701,UPTIM1701,UPUSM1701)
                                values 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                """,(headerId, getName, appId, appName,kategori, getQuery ,status,joinTo, isExist, date, time, user, date, time, user))
                

                    
            for el in data['field']:
                    fieldName = ''
                    
                    if type(el['extFname']) == dict:
                        fieldName = el['extFname']['key']
                    else :
                        fieldName = el['extFname']
                    
                    fieldId = el['fieldName'].upper()
                    daType = el['datTypeField'].upper()
                    maxVal = el['maxlenField']
                    isPk = '1' if el['isPk'] else '0'
                        
                    cur_sql.execute("""
                                    INSERT INTO AAM1801 (FEIDM1801,HEIDM1801,NMCAM1801,DEVAM1801,DATYM1801,ISPKM1801,EXTDM1801,CRDTM1801,CRTMM1801,CRUSM1801,UPDTM1801,UPTIM1801,UPUSM1801,STATM1801)
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
            # msg['message'] = 'Error'
            
                        # DB_SQL.commit()
                    #     return jsonify(msg)
                    # else:
                    #     return jsonify(msg)
            DB_SQL.commit()
        return jsonify(msg)
    
    
@master_dbds_ext.route('/api/master_dbds_ext/<string:id>', methods=["GET",'PUT'])
def putExtTable(id):
    token = request.headers['Authorization']
    appCode = decrypt_text(request.headers['App'].encode())
    auth_page = check_user_auth_page(token, appCode, module_id)
    if not auth_page:
        return jsonify({'message': 'Token Invalid'}), 403
    else:
        auth_page = auth_page.get_json()
        auth_page = list(auth_page)
    user = check_user(token, amg = True)
    
    date = datetime.now()
    time = date.strftime("%H%M")
    date = date.strftime("%Y%m%d")
    user = 'santoso'
    
    if request.method == 'GET':
        # if auth_page[0] != '1':
        #         return jsonify({'message': 'Not Authorized'}), 401
        
        cur_sql.execute("""
            SELECT
                TBIDM1701 as table_id ,
                CPTBM1701 as caption_table,
                APNOM1701 as aplication_id,
                APNAM1701 as aplication_name,        
                KTAPM1701 as kategori_app,
                QESRM1701 as query_string,
                JOINM1701 as joinTo ,
                EXTTM1701 as isExist 
            from AAM1701
            where TBIDM1701 = %s
            """, (id,))
        result1 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]

        
        cur_sql.execute("""
            SELECT 
                FEIDM1801 as field_id,
                HEIDM1801 as header_id,
                NMCAM1801 as name_caption,
                DEVAM1801 as default_value,
                DATYM1801 as data_type,
                ISPKM1801 as statPk,
                EXTDM1801 
                as isExistField,
                STATM1801 as 'statTD'
            FROM AAM1801
            where HEIDM1801 = %s AND STATM1801 = 'active'
            """,(id,))
        result2 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]

        result_dict = {'table_data': result1, 'field_data': result2}
    
        return jsonify(result_dict)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        headerId = id
        date = datetime.now()
        time = date.strftime("%H%M")
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
                UPDATE AAM1701
                SET
                    CPTBM1701 = %s,
                    APNOM1701 = %s,
                    APNAM1701 = %s,        
                    KTAPM1701 = %s,
                    QESRM1701 = %s,
                    HISTM1701 = %s,
                    UPDTM1701 = %s,
                    UPTIM1701 = %s,
                    UPUSM1701 = %s
                WHERE
                    TBIDM1701 = %s
                """,(data['tableName'], appId, appName, kategori, newCreatedQuery, editedQuery, date, time, user,headerId))
        
        DB_SQL.commit()
        
        cur_sql.execute("""
            SELECT 
                FEIDM1801 as field_id,
                HEIDM1801 as header_id,
                NMCAM1801 as name_caption,
                DEVAM1801 as default_value,
                DATYM1801 as data_type,
                ISPKM1801 as statPk,
                STATM1801 as 'statTD'
            FROM AAM1801
            where HEIDM1801 = %s AND STATM1801 = 'active'
            """,(id,))
        oldDatas = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        oldLen = len(oldDatas)
        newLen = len(data['field'])
        
        if oldLen != newLen:
            newFields = data['field'][oldLen: newLen]
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
                                    INSERT INTO AAM1801 (FEIDM1801,HEIDM1801,NMCAM1801,DEVAM1801,DATYM1801,ISPKM1801,EXTDM1801,CRDTM1801,CRTMM1801,CRUSM1801,UPDTM1801,UPTIM1801,UPUSM1801, STATM1801)
                                    values (%s , %s , %s , %s , %s , %s , %s , %s , %s ,%s, %s, %s,%s, %s);
                                    """,(newIds,headerId,fieldName,newMaxVal,newDat,isPk,isExist,date, time, user, date, time, user,stat))
                    DB_SQL.commit()
            else:
                #  removedField = old['field_data'][len(inputNew['field']):len(old['field_data'])]
                removeField = oldDatas[newLen : oldLen]
                for x in removeField:
                    removedId = x['field_id']
                    cur_sql.execute("""
                                    UPDATE AAM1801
                                    SET 
                                        STATM1801 = 'inactive'
                                    WHERE 
                                        FEIDM1801 = '{ids}'
                                    """.format(ids=removedId))
                    DB_SQL.commit()
                    
                    
                
        else:
            for el in data['field']:
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
                            UPDATE AAM1801
                            SET
                                HEIDM1801 = %s,
                                NMCAM1801 = %s,        
                                DEVAM1801 = %s,
                                DATYM1801 = %s,
                                ISPKM1801 = %s,
                                EXTDM1801 = %s,
                                STATM1801 = %s,
                                UPDTM1801 = %s,
                                UPTIM1801 = %s,
                                UPUSM1801 = %s
                            WHERE
                                FEIDM1801 = %s
                            """,(headerId,fieldName,maxlen,daType,isPk,isExist,statTD,date, time, user,fieldId))
                DB_SQL.commit()
 
        return jsonify(0)