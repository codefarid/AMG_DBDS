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
            return 'TBIDM1701'
        case 'caption':
            return 'CPTBM1701'
        case 'query':
            return 'QESRM1701'
        case 'status':
            return 'STATM1701'
        
    return 'TBIDM1701'

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
        param = request.args.to_dict()
        where = ''
        
        if param['globalFilter'] != 'null':
            where = '''WHERE
                            STATM1701 = 'active' AND
                            (TBIDM1701 like '%{filter}%' OR
                            CPTBM1701 like '%{filter}%' OR
                            QESRM1701 like '%{filter}%')  
                    '''.format(filter = param['globalFilter'])
        else:
            where = '''
                    WHERE STATM1701 = 'active'
                    '''
        if param['filteredApp'] != 'null':
            where = f'''WHERE APNAM1701 = '{param['filteredApp']}' and STATM1701 = 'active' '''
        cur_sql.execute("""
                    SELECT 
                        COUNT(*) AS totalData
                    FROM {table} {where}
                """.format(table='AAM1701', where=where))

        totalData = cur_sql.fetchone()[0]
        orderByCol = "LEN(TBIDM1701)"#checkColumn(param['orderBy'])
        orderByMethod = "ASC"#param['orderMethod']
        
        cur_sql.execute("""
                        Select 
                            TBIDM1701 as 'id',
                            CPTBM1701 as 'caption',
                            QESRM1701 as 'query',
                            STATM1701 as 'status',
                            EXTTM1701 as 'isExisting',
                            APNAM1701 as 'aplication',
                            KTAPM1701 as 'categories',
                            JOINM1701 as 'joined'
                            from AAM1701 
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
        data = request.get_json()
        
        
        headerId = generateIdHeader(data)
        cur_sql.execute("""
                        select 
                        TBIDM1701 as table_id ,  
                            CPTBM1701 as caption_table,
                            APNOM1701 as aplication_id,
                            APNAM1701 as aplication_name,
                            KTAPM1701 as kategori_app
                        from AAM1701
                        """)
        checkData = []
        for row in cur_sql:
            checkData.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

        for el in checkData:
            if headerId == el['table_id']:
                cur_sql.execute("""
                                SELECT TBIDM1701 AS table_id
                                FROM AAM1701
                                """)
                existingIds = [row[0] for row in cur_sql]
                
                while headerId in existingIds:
                    gg = headerId[0:-1] + str(int(headerId[-1]) + 1)
                    headerId = gg
        
        date = datetime.now()
        time = date.strftime("%H%M")
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
            INSERT INTO AAM1701 (
                TBIDM1701,
                CPTBM1701,
                APNOM1701,
                APNAM1701,
                KTAPM1701,
                QESRM1701,
                STATM1701,
                JOINM1701,
                EXTTM1701,
                CRDTM1701,
                CRTMM1701,
                CRUSM1701,
                UPDTM1701,
                UPTIM1701,
                UPUSM1701
                )
            values (
                %s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                
                )
            """,(headerId,
                 data['tableName'],
                 appId, 
                 appName,
                 kategori,
                 getQuery,
                 status,
                 joinTo,
                 isExist,
                 date, 
                 time,
                 user,
                 date,
                 time,
                 user
                 ))


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
                INSERT INTO AAM1801 (
                    FEIDM1801,
                    HEIDM1801,
                    NMCAM1801,
                    DEVAM1801,
                    DATYM1801,
                    ISPKM1801,
                    EXTDM1801,
                    CRDTM1801,
                    CRTMM1801,
                    CRUSM1801,
                    UPDTM1801,
                    UPTIM1801,
                    UPUSM1801,
                    STATM1801,
                    ISFKM1801,
                    FKTOM1801)
                values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s);
                """,(
                    fieldId,
                    headerId,
                    daType,
                    fieldName,
                    maxVal,
                    isExist,
                    isFK,
                    isFKto,
                    isPk,
                    status,
                    date, 
                    time, 
                    user, 
                    date, 
                    time, 
                    user
                    ))

        DB_SQL.commit()
        return jsonify(0)

@master_dbds.route('/api/master_dbds/dropdown/<string:appName>')
def filterByApp(appName):
    query = ''
    if appName != 'null':
        query = f"""
                        Select 
                                TBIDM1701 as 'id',
                                CPTBM1701 as 'caption',
                                QESRM1701 as 'query',
                                STATM1701 as 'status',
                                EXTTM1701 as 'isExisting',
                                APNAM1701 as 'aplication',
                                KTAPM1701 as 'categories',
                                JOINM1701 as 'joined'
                                from AAM1701
                        WHERE APNAM1701 = '{appName}' and STATM1701 = 'active'
                        """
    else:
        query = """
                        Select 
                                TBIDM1701 as 'id',
                                CPTBM1701 as 'caption',
                                QESRM1701 as 'query',
                                STATM1701 as 'status',
                                EXTTM1701 as 'isExisting',
                                APNAM1701 as 'aplication',
                                KTAPM1701 as 'categories',
                                JOINM1701 as 'joined'
                                from AAM1701
                        WHERE STATM1701 = 'active'
                        """
    
    cur_sql.execute(query)
    results = []
    for row in cur_sql:
        results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

    getFields = getFieldsPerTable(results)

    totalData = len(results)
    return jsonify({ "totalRecord": totalData, "result":results, "fields":getFields})
    
@master_dbds.route('/api/master_dbds/<string:id>', methods=['GET', 'PUT'])
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
                EXTDM1801 as isExistField,
                STATM1801 as status,
                ISFKM1801 as isFK,
                FKTOM1801 as isFKto
            FROM AAM1801
            where HEIDM1801 = %s AND STATM1801 = 'active'
            """,(id,))
        result2 = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        
        result3 = "SELECT?"
        
        for x in result2:
                result3 += f"{x['field_id']} as '{x['name_caption']}'?"
        
        result3 += f'FROM {result1[0]["table_id"]}?'

        # result4 = f'CREATE TABLE {result2[0]["header_id"]} (?'
        # for y in result2:
        #         if y['default_value'] != '0':
        #             result4 += f'{y["field_id"]} {y["data_type"]}({y["default_value"]})?'
        #         elif y['default_value'] != None:
        #             result4 += f'{y["field_id"]} {y["data_type"]}({y["default_value"]})?'
        #         else:
        #             result4 += f'{y["field_id"]} {y["data_type"]}?'
        
        # for z in result2:
        #     if z['isFK'] != "0" and z['isFKto'] != "0":
        #         result4 += f'CONSTRAINT FK_{z["field_id"]} FOREIGN KEY ({z["field_id"]}) REFERENCES {z["isFKto"]}({z["isFK"]})'
        
                    
        # result4 += ')?'
        
        result_dict = {'table_data': result1, 'field_data': result2, 'selecQuery': result3}
        # print(result_dict)
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
                """,(
                    data['tableName'],
                    appId,
                    appName,
                    kategori,
                    newCreatedQuery,
                    editedQuery, 
                    date,
                    time,
                    user,
                    headerId
                    ))
        
        DB_SQL.commit()
        
        cur_sql.execute("""
            SELECT 
                FEIDM1801 as field_id,
                HEIDM1801 as header_id,
                NMCAM1801 as name_caption,
                DEVAM1801 as default_value,
                DATYM1801 as data_type,
                ISPKM1801 as statPk,
                STATM1801 as statusTD,
                ISFKM1801 as isFK,
                FKTOM1801 as isFKto
            FROM AAM1801
            where HEIDM1801 = %s and STATM1801 = 'active'
            """,(id,))
        oldDatas = [dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])) for row in cur_sql]
        oldLen = len(oldDatas)
        newLen = len(data['field'])
        
        if oldLen != newLen:
            if oldLen < newLen:
                newFields = data['field'][oldLen: newLen]
                for y in newFields:
                    newIds = generateIdTDetail(y['fieldNameEdit']['value'], id)
                    fieldName = y['fieldNameEdit']['key']
                    newDat = y['datTypeField'].upper()
                    newMaxVal = y['maxlenField']
                    statusTD = y['statTD']
                    isFK = y['isFK']["value"] if y['isFK']["value"] else '0'
                    isFKto = y['isFKto']['value'] if y['isFKto']['value'] else '0'
                    
                    isPk = '1' if y['isPk'] else '0'
                    
                    cur_sql.execute("""
                                    INSERT INTO AAM1801 (
                                        FEIDM1801,
                                        HEIDM1801,
                                        DATYM1801,
                                        NMCAM1801,
                                        DEVAM1801,
                                        EXTDM1801,
                                        ISFKM1801,
                                        FKTOM1801,
                                        ISPKM1801,
                                        STATM1801,
                                        CRDTM1801,
                                        CRTMM1801,
                                        CRUSM1801,
                                        UPDTM1801,
                                        UPTIM1801,
                                        UPUSM1801)
                                    values (
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s ,
                                        %s );
                                    """,(
                                        newIds,
                                        headerId,
                                        newDat,
                                        fieldName,
                                        newMaxVal,
                                        isExist,
                                        isFK,
                                        isFKto,
                                        isPk,
                                        statusTD,
                                        date,
                                        time,
                                        user,
                                        date,
                                        time,
                                        user,
                                        ))
                    DB_SQL.commit()
        else:
            for el in data['field']:
                fieldId = generateIdTDetail(el['fieldNameEdit']['value'], id)
                fieldName = el['fieldNameEdit']['key']
                    
                daType = el['datTypeField'].upper()
                maxlen = el['maxlenField']
                isPk = '1' if el['isPk'] else '0'
                statTD = el['statTD']
                isFK = el['isFK']["value"]
                isFkto = el['isFKto']["value"]
                
                
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
                                UPUSM1801 = %s,
                                ISFKM1801 = %s,
                                FKTOM1801 = %s
                            WHERE
                                FEIDM1801 = %s
                            """,(
                                headerId,
                                 fieldName,
                                 maxlen,
                                 daType,
                                 isPk,
                                 isExist,
                                 statTD,
                                 date, 
                                 time, 
                                 user,
                                 isFK,
                                 isFKto,
                                 fieldId
                                 ))
                DB_SQL.commit()
 
        return jsonify(0)
                
@master_dbds.route('/api/master_dbds/<string:id>', methods=['DELETE'])
def deleteTable(id):
    cur_sql.execute("""
                    UPDATE AAM1701
                    SET STATM1701 = 'inactive' 
                    WHERE TBIDM1701 = %s
                    """, (id,))
    DB_SQL.commit()
    return jsonify("Status Change!")

@master_dbds.route('/api/master_dbds/fetch/<string:appName>',methods=['GET'])
def getDDbyApp(appName):
    db = ""
    if test == True:
        db = "TestAMGAPPS"
    else:
        db = "AMGAPPS"
        
    cur_sql.execute(f"""
                    use {db}
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE='BASE TABLE' 
                    AND TABLE_NAME LIKE '%{appName}%'
                    order by TABLE_NAME ASC
                    """)
    t = []
    for row in cur_sql:
        t.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
    
    return jsonify({"msg":"wait",'data':t})


@master_dbds.route('/api/master_dbds/post/downloads',methods=['POST'])
def downloadFile():
    token = request.headers['Authorization']
    user = check_user(token, amg = True)
    data = request.get_json()
    now = datetime.now()
    nameFile = f'{user}-querries-{len(data)}-{now.strftime("%d%m%y-%H%I")}.sql'
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
        