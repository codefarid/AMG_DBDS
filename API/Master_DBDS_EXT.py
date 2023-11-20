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
                                values ('{headerId}','{getName}','{appId}','{appName}','{kategori}','{getQuery}','{status}','{joinTo}','{isExist}','{dates}','{times}','{users}','{date}','{time}','{user}')
                                """.format( headerId = headerId, getName = getName, appId = appId, appName = appName, kategori = kategori, getQuery = getQuery, status = status, joinTo = joinTo, isExist = isExist, dates = date, times = time, users = user, date = date, time = time, user = user))
                

                    
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
                                    values ('{fieldId}','{headerId}','{fieldName}','{maxVal}','{daType}','{isPk}','{isExist}','{dates}','{times}','{users}','{date}','{time}','{user}','{status}')
                                    """.format(fieldId = fieldId,headerId = headerId,fieldName = fieldName,maxVal = maxVal,daType = daType,isPk = isPk,isExist = isExist ,dates = date,times = time,users = user,date = date,time = time,user = user,status = status))
                    

            msg['message'] = 'Sukes menambahkan Tabel!'
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
            where TBIDM1701 = '{id}'
            """.format(id = id))
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
            where HEIDM1801 = '{id}' AND STATM1801 = 'active'
            """.format(id = id,))
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
                    CPTBM1701 =  '{data}',
                    APNOM1701 =  '{appId}',
                    APNAM1701 =  '{appName}',
                    KTAPM1701 =  '{kategori}',
                    QESRM1701 =  '{newCreatedQuery}',
                    HISTM1701 =  '{editedQuery}',
                    UPDTM1701 =  '{date}',
                    UPTIM1701 =  '{time}',
                    UPUSM1701 =  '{user}'
                WHERE
                    TBIDM1701 = '{headerId}'
                """.format(
                    data = data['tableName'],
                    appId = appId,
                    appName = appName,
                    kategori = kategori,
                    newCreatedQuery = newCreatedQuery,
                    editedQuery = editedQuery,
                    date = date,
                    time = time,
                    user = user,
                    headerId = headerId)
                )

        
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
            where HEIDM1801 = '{id}' AND STATM1801 = 'active'
            """.format(id = id,))
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
                                    INSERT INTO AAM1801 (FEIDM1801,HEIDM1801,NMCAM1801,DEVAM1801,DATYM1801,ISPKM1801,EXTDM1801,CRDTM1801,CRTMM1801,CRUSM1801,UPDTM1801,UPTIM1801,UPUSM1801,STATM1801)
                                    values ('{newIds}','{headerId}','{fieldName}','{newMaxVal}','{newDat}','{isPk}','{isExist}','{dates}','{times}','{users}','{date}','{time}','{user}','{stat}')
                                    """.format(newIds = newIds,headerId = headerId,fieldName = fieldName,newMaxVal = newMaxVal,newDat = newDat,isPk = isPk,isExist = isExist,dates = date,times = time,users = user,date = date,time = time,user = user,stat = stat))
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
                # fieldId = generateIdTDetail(y['fieldNameEdit']['value'],
                #  id)
                # fieldName = el['fieldNameEdit']['key']
                    
                daType = el['datTypeField'].upper()
                maxlen = el['maxlenField']
                isPk = '1' if el['isPk'] else '0'
                statTD = el['statTD']
                
                cur_sql.execute("""
                            UPDATE AAM1801
                            SET
                                HEIDM1801 = '{headerId}',
                                NMCAM1801 = '{fieldName}',        
                                DEVAM1801 = '{maxlen}',
                                DATYM1801 = '{daType}',
                                ISPKM1801 = '{isPk}',
                                EXTDM1801 = '{isExist}',
                                STATM1801 = '{statTD}',
                                UPDTM1801 = '{date}',
                                UPTIM1801 = '{time}',
                                UPUSM1801 = '{user}'
                            WHERE
                                FEIDM1801 = '{fieldId}'
                            """.format(
                                headerId = headerId,
                                fieldName = fieldName,
                                maxlen = maxlen,
                                daType = daType,
                                isPk = isPk,
                                isExist = isExist,
                                statTD = statTD,
                                date = date,
                                time = time,
                                user = user,
                                fieldId = fieldId)
                            )

                DB_SQL.commit()
 
        return jsonify(0)