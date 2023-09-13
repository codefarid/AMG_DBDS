import os
from flask import Blueprint, jsonify, request , send_file, Response
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

module_id = 1

@master_dbds.route('/api/master_dbds', methods=['GET', 'POST'])
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
        orderByCol = "LEN(AAMTBIDZ1302)"#checkColumn(param['orderBy'])
        orderByMethod = "ASC"#param['orderMethod']
        
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
        # user = "santoso"
        date = date.strftime("%Y%m%d")
        isExist = '0'
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

        # DB_SQL.commit()

        for el in data['field']:
            fieldName = el['fieldName']['key']
            fieldId = generateIdTDetail(el['fieldName']['value'], headerId)
            daType = el['datTypeField'].upper()
            maxVal = el['maxlenField']
            isPk = '1' if el['isPk'] else '0'
            isFK = el['isFK'] if el['isFK'] else '0'
            isFKto = el['isFKto'] if el['isFKto'] else '0'
            status = 'active'

            cur_sql.execute("""
                INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302,AAMSTTDZ1301,AAMISFKZ1301,AAMFKTOZ1301)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,(fieldId,headerId,fieldName,maxVal,daType,isPk,isExist,date, time, user, date, time, user,status,isFK,isFKto))

        DB_SQL.commit()
        return jsonify(0)

    
@master_dbds.route('/api/master_dbds/<string:id>', methods=['GET', 'PUT'])
# @check_for_token
def getOneTable(id):
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
                AAMSTTDZ1301 as status,
                AAMISFKZ1301 as isFK,
                AAMFKTOZ1301 as isFKto
            FROM AAMTBDTZ1301
            where AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
            """,(id,))
        result2 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        
        result3 = "SELECT?"
        
        for x in result2:
                result3 += f"{x['field_id']} as '{x['name_caption']}'?"
        
        result3 += f'FROM {result1[0]["table_id"]}?'

        result4 = f'CREATE TABLE {result2[0]["header_id"]} (?'
        for y in result2:
                if y['default_value'] != '0':
                    result4 += f'{y["field_id"]} {y["data_type"]}({y["default_value"]})?'
                elif y['default_value'] != None:
                    result4 += f'{y["field_id"]} {y["data_type"]}({y["default_value"]})?'
                else:
                    result4 += f'{y["field_id"]} {y["data_type"]}?'
        
        for z in result2:
            if z['isFK'] != "0" and z['isFKto'] != "0":
                result4 += f'CONSTRAINT FK_{z["field_id"]} FOREIGN KEY ({z["field_id"]}) REFERENCES {z["isFKto"]}({z["isFK"]})'
        
                    
        result4 += ')?'
        
        result_dict = {'table_data': result1, 'field_data': result2, 'selecQuery': result3,'createdQuery':result4}
    
        return jsonify(result_dict)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        headerId = id
        date = datetime.now()
        time = date.strftime("%H%M")
        # user = "santoso"
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
                AAMSTTDZ1301 as statusTD,
                AAMISFKZ1301 as isFK,
                AAMFKTOZ1301 as isFKto
            FROM AAMTBDTZ1301
            where AAMHAIDZ1302 = %s and AAMSTTDZ1301 = 'active'
            """,(id,))
        oldDatas = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        oldLen = len(oldDatas)
        newLen = len(data['field'])
        
        if oldLen != newLen:
            if oldLen < newLen:
                newFields = data['field'][oldLen: newLen]
                # print(newFields,"????????????????")
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
                    isFK = y['isFK']["value"] if y['isFK']["value"] else '0'
                    isFKto = y['isFKto']['value'] if y['isFKto']['value'] else '0'
                    
                    isPk = '1' if y['isPk'] else '0'
                    
                    cur_sql.execute("""
                                    INSERT INTO AAMTBDTZ1301 (AAMFEIDZ1302,AAMHAIDZ1302,AAMNMZ1302,AAMVLZ1302,AAMDTZ1302,AAMPKZ1302,AAMEXTDZ1301,AAMCEATZ1302,AAMCETMZ1302,AAMCEUEZ1302,AAMUDATZ1302,AAMUDTMZ1302,AAMUDUEZ1302, AAMSTTDZ1301, AAMISFKZ1301 ,AAMFKTOZ1301)
                                    values (%s , %s , %s , %s , %s , %s , %s , %s , %s ,%s, %s, %s,%s,%s);
                                    """,(newIds,headerId,fieldName,newMaxVal,newDat,isPk,isExist,date, time, user, date, time, user,statusTD,isFK,isFKto))
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
                # print(el,"<><><><><><")
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
                isFK = el['isFK']["value"]
                isFkto = el['isFKto']["value"]
                
                
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
                                AAMUDUEZ1302 = %s,
                                AAMISFKZ1301 = %s,
                                AAMFKTOZ1301 = %s
                            WHERE
                                AAMFEIDZ1302 = %s
                            """,(headerId,fieldName,maxlen,daType,isPk,isExist,statTD,date, time, user,fieldId, isFK,isFKto))
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

@master_dbds.route('/api/master_dbds/post/downloads',methods=['POST'])
def downloadFile():
    data = request.get_json()
    now = datetime.now()
    nameFile = f'querries-{len(data)}-{now.strftime("%d%m%y-%H%I")}.sql'
    storePath = "./temp"
    filePath = os.path.join(storePath,nameFile)
    if request.method == "POST":
        if len(data) == 0:
            return jsonify({"msg":"No Data!"})
        with open(filePath,"w") as file:
            for query in data:
                file.write(query + "\n") 
        
        url = ''
        
        local = "http://127.0.0.1:5006/"; 
        dbds_test = "http://172.18.178.242:5017/"; 
        if development:
            url = f'{local}api/master_dbds/downloads/{nameFile}'
        else:
            url = f'{dbds_test}api/master_dbds/downloads/{nameFile}'
        
        return jsonify({"msg":"OKE","fileName":nameFile, "download_url":url})
    # if request.method == "GET":
        
@master_dbds.route('/api/master_dbds/downloads/<fileName>')
def getDownloadFile(fileName):
    try:
        storePath = "./temp"
        filePath = os.path.join(storePath, fileName)
        if os.path.exists(filePath):
            size = os.path.getsize(filePath)
            capacity = ''
            divided = 0
            if size <= 1099511627776:
                capacity = 'GB'
                divided = size / ( 1024 * 1024 * 1024) 
            if size <= 1073741824:
                capacity = "MB"
                divided = size / ( 1024 * 1024 ) 
            if size <= 1048576:
                capacity = 'KB'
                divided = size / 1024 
            if size <= 1024:
                capacity = "B"
                divided = size
            print(round(divided),capacity)
            def generate():
                with open(filePath,'rb') as file:
                    while True:
                        chunk = file.read(4096)
                        if not chunk:
                            break
                        yield chunk
            return Response(generate(),content_type='aplication/octet-stream', headers={"Content-Disposition":f"attachment; filename={fileName}"})
        else:
            return jsonify({"msg": f"File '{fileName}' not found."}), 404    
    except Exception as e:
        print(str(e))
        return jsonify({"msg": str(e)}), 500

@master_dbds.route('/api/master_dbds/delete/downloads/<fileName>',methods=['GET'])
def deleteFiles(fileName):
    print(fileName)
    if os.path.exists(f'./temp/{fileName}'):
        os.remove(f'./temp/{fileName}')
        return jsonify({"msg":f"Deleted {fileName}"})
    else:
        print("The file does not exist")
        return jsonify({"msg":"The file does not exist"})
        