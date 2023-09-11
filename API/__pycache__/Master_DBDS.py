import os
from flask import Blueprint, Response, jsonify, json, request
from DB import *
from Helpers import *
from datetime import datetime
from Decorators import *

master_dbds = Blueprint('master_dbds',__name__)

def checkColumn(alias):
    match alias:
        case 'id':
            return 'AAMTBIDZ1302'
        case 'caption':
            return 'AAMCPTBZ1302'
        case 'query':
            return 'AAMQESRZ1302'
        case 'status':
            return 'AAMTHSTZ1302'
        
    return 'AAMTBIDZ1302'


@master_dbds.route('/api/master_dbds', methods=['GET', 'POST'])
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
        # if auth_page[0] != '1':
        #     return jsonify({'message': 'Not Authorized'}), 401
        param = request.args.to_dict()
        where = ''
        
        if param['globalFilter'] != 'null':
            where = '''WHERE
                            AAMTHSTZ1302 = 'active' AND
                            (AAMTBIDZ1302 like '%{filter}%' OR
                            AAMCPTBZ1302 like '%{filter}%' OR
                            AAMQESRZ1302 like '%{filter}%')  
                           
                    '''.format(filter = param['globalFilter'])
        else:
            where = '''
                    WHERE AAMTHSTZ1302 = 'active'
                    '''
        cur_sql.execute("""
                    SELECT 
                        COUNT(*) AS totalData
                    FROM {table} {where}
                """.format(table='AAMTBHAZ1301', where=where))

        totalData = cur_sql.fetchone()[0]
        orderByCol = checkColumn(param['orderBy'])
        orderByMethod = param['orderMethod']
        
        cur_sql.execute("""
                        Select 
                            AAMTBIDZ1302 as 'id',
                            AAMCPTBZ1302 as 'caption',
                            AAMQESRZ1302 as 'query',
                            AAMTHSTZ1302 as 'status',
                            AAMEXTTZ1301 as 'isExisting',
                            AAMALNMZ1302 as 'aplication',
                            AAMKTAPZ1302 as 'categories',
                            AAMJOINZ1302 as 'joined'
                            from AAMTBHAZ1301 
                            {where}
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

        getFields = getFieldsPerTable(results)
                   
        
        data = {
            "totalRecord": totalData,
            "result" : results,
            "fields": getFields
        }
     
        return jsonify(data)
    
    if request.method == "POST":
        # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401
        
        data = request.get_json()
        
        
        headerId = generateIdHeader(data)
        cur_sql.execute("""
                        select 
                        AAMTBIDZ1302 as table_id ,  
                            AAMCPTBZ1302 as caption_table,
                            AAMALIDZ1302 as aplication_id,
                            AAMALNMZ1302 as aplication_name,
                            AAMKTAPZ1302 as kategori_app
                        from AAMTBHAZ1301
                        """)
        checkData = []
        for row in cur_sql:
            checkData.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
        # print(checkData)
        for el in checkData:
            if headerId == el['table_id']:
                cur_sql.execute("""
                                SELECT AAMTBIDZ1302 AS table_id
                                FROM AAMTBHAZ1301
                                """)
                existingIds = [row[0] for row in cur_sql]
                
                while headerId in existingIds:
                    gg = headerId[0:-1] + str(int(headerId[-1]) + 1)
                    headerId = gg
            
        print(headerId,"SINI IIIIII")
        
        date = datetime.now()
        time = date.strftime("%H%M")
        user = "santoso"
        date = date.strftime("%Y%m%d")
        isExist = '0'
        
        # cur_sql.execute("""
        #                 Select AAMCPTBZ1302 as caption from AAMTBHAZ1301 where AAMCPTBZ1302 like '%{name}%'
        #                 """.format(name = data['tableName']))
        
        # rows = cur_sql.fetchall()
        # if len(rows) > 0:
        #     table_names = rows[0][0]
        #     if table_names.upper() == data['tableName'].upper():
        #         return jsonify({'message':"Nama Table Sudah Ada, Buat Nama Table lain!"})
        # else:
        #     table_names = ['']       
        # if len(table_names) > 0 and data['tableName'] in table_names:
        #     return jsonify({'message':"Nama Table Sudah Ada, Buat Nama Table lain!"})
        # else:
        appName = data['appName']['text']
        kategori = data['isMaster']['value']
        getQuery = postQuery(data)
        cur_sql.execute("""
            Select AMAPCA101 as 'app_id' from AAM101
                WHERE AMAPNA101 = '{appName}'
            """.format(appName = appName))
        results = cur_sql.fetchall()
        appId = results[0][0]
        status = "active"
        joinTo = data['joinTo']


        cur_sql.execute("""
            INSERT INTO AAMTBHAZ1301 (AAMTBIDZ1302,AAMCPTBZ1302,AAMALIDZ1302,AAMALNMZ1302,AAMKTAPZ1302,AAMQESRZ1302,AAMTHSTZ1302,AAMJOINZ1302,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302 ,AAMEXTTZ1301)
            values 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(headerId, data['tableName'], appId, appName,kategori, getQuery ,status,joinTo, date, time, user, date, time, user, isExist))

        DB_SQL.commit()

        for el in data['field']:
            fieldName = el['fieldName']['key']
            fieldId = generateIdTDetail(el['fieldName']['value'], headerId)
            daType = el['datTypeField'].upper()
            maxVal = el['maxlenField']
            isPk = '1' if el['isPk'] else '0'
            status = 'active'

            cur_sql.execute("""
                INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302,AAMSTTDZ1301)
                values (%s , %s , %s , %s , %s , %s , %s , %s , %s ,%s, %s, %s,%s,%s);
                """,(fieldId,headerId,fieldName,maxVal,daType,isPk,isExist,date, time, user, date, time, user,status))

        DB_SQL.commit()
        return jsonify(0)

    
@master_dbds.route('/api/master_dbds/<string:id>', methods=['GET', 'PUT'])
# @check_for_token
def getOneTable(id):
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
                AAMSTTDZ1301 as status
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
        isExist = '0'
        
        cur_sql.execute("""
                            Select AMAPCA101 as 'app_id' from AAM101
                                WHERE AMAPNA101 = '{appName}'
                            """.format(appName = appName))
        results = cur_sql.fetchall()
        appId = results[0][0]
        
        editedQuery = editQuery(data, headerId)
        newCreatedQuery = editedPostQuery(data)
        
        
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
                AAMSTTDZ1301 as statusTD
            FROM AAMTBDTZ1301
            where AAMHAIDZ1302 = %s and AAMSTTDZ1301 = 'active'
            """,(id,))
        oldDatas = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        oldLen = len(oldDatas)
        newLen = len(data['field'])
        
        if oldLen != newLen:
            if oldLen < newLen:
                newFields = data['field'][oldLen: newLen]
                print(newFields,"????????????????")
                for y in newFields:
                    # if y['extFname']['key']:
                    #     fieldName =  y['extFname']['key']
                    # else:
                    #     fieldName = y['extFname']
                    # if y['editFieldName']['value']:
                    #     newIds = generateIdTDetail(y['fieldNameEdit']['value'], id)
                    # else:
                    #     newIds = y['fieldName'].upper()
                    newIds = generateIdTDetail(y['fieldNameEdit']['value'], id)
                    fieldName = y['fieldNameEdit']['key']
                    newDat = y['datTypeField'].upper()
                    newMaxVal = y['maxlenField']
                    statusTD = y['statTD']
                    
                    isPk = '1' if y['isPk'] else '0'
                    
                    cur_sql.execute("""
                                    INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302, AAMSTTDZ1301)
                                    values (%s , %s , %s , %s , %s , %s , %s , %s , %s ,%s, %s, %s,%s,%s);
                                    """,(newIds,headerId,fieldName,newMaxVal,newDat,isPk,isExist,date, time, user, date, time, user,statusTD))
                    DB_SQL.commit()
            # else:
            #     removeField = oldDatas[newLen : oldLen]
            #     for x in removeField:
            #         removedId = x['field_id']
            #         cur_sql.execute("""
            #                         UPDATE AAMTBDTZ1301
            #                         SET 
            #                             AAMSTTDZ1301 = 'inactive'
            #                         WHERE 
            #                             AAMFEIDZ1302 = '{ids}'
            #                         """.format(ids=removedId))
            #         DB_SQL.commit()
                    
                # print(removeField,'?? PUT REMOVE FIELD Master TABLE')
        else:
            for el in data['field']:
                print(el,"<><><><><><")
                # fieldName = ''
                # fieldId = ''
                # if el['extFname']['key']:
                #     fieldName = el['extFname']['key']
                # else:
                #     fieldName = el['fieldName']['key']
                    
                # if el['fieldName']['value']:
                #     fieldId = el['fieldName']['value'].upper()
                # else:
                #     fieldId = el['fieldName'].upper()
                fieldId = generateIdTDetail(el['fieldNameEdit']['value'], id)
                fieldName = el['fieldNameEdit']['key']
                    
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
                

@master_dbds.route('/api/master_dbds/<string:id>', methods=['DELETE'])
def deleteTable(id):
    # if '1' not in auth_page[1:]:
        #     return jsonify({'message': 'Not Authorized'}), 401
    cur_sql.execute("""
                    UPDATE AAMTBHAZ1301
                    SET AAMTHSTZ1302 = 'inactive' 
                    WHERE AAMTBIDZ1302 = %s
                    """, (id,))
    DB_SQL.commit()
    return jsonify("Status Change!")

