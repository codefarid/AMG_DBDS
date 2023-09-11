from DB import *

def recreateObj(obj):
    wy = [data for data in obj['field'] if data['statTD'] == 'active']
    temp = {
        "tableName": obj['tableName'],
        "extTableName": obj['extTableName'],
        "isMaster": obj['isMaster'],
        "extName": obj['extName'],
        "appName": obj['appName'],
        "joinTo": obj['joinTo'],
        "status": obj['status'],
        "isExisted": obj['isExisted'],
        "field": wy
    }
    return temp

def renameCol(headerId, oldId, newId):
    print("======== Rename Field From Table ",headerId," ==================")
    result = 'ALTER TABLE ' + headerId + ' RENAME ' + oldId + ' TO ' + newId
    
    print("\t", oldId, " Renamed to ", newId,  " returning string = ", result)
    print("================================================================")
    
    return result

def editDaType(headerId, fieldId, datType, defVal):
    print("========= Edit Data Type Field From Table ", headerId, " =======")
    
    result = 'ALTER TABLE ' + headerId + ' ALTER COLUMN ' + fieldId + ' ' + datType + '(' + defVal + ')'
    print("Returning String = \n", result)
    print("================================================================")
    return result

def detectPkChange(newData,headerId):
    
    query = ''    
    cur_sql.execute("""
                SELECT 
                    AAMFEIDZ1302 as fieldId,
                    AAMHAIDZ1302 as headerId,
                    AAMVLZ1302 as defaultValue,
                    AAMDTZ1302 as dataType,
                    AAMPKZ1302 as isPk,
                    AAMSTTDZ1301 as statuses
                FROM AAMTBDTZ1301
                where AAMHAIDZ1302 = %s and AAMPKZ1302 = '1' and AAMSTTDZ1301 = 'active'
                """, (headerId,))
    oldField = [dict(zip([column[0] for column in cur_sql.description], [
                    str(x).strip() for x in row])) for row in cur_sql]
    
      
    newField = []
    for obj in newData['field']:
        if obj['isPk'] == True:
            newField.append(obj)   

    newId =  newField[0]['fieldName']
    oldId = oldField[0]['fieldId']  
    print("Detect Renaming condition")
    newIds = newId['value']
    print("New field id contain pk is = ", newIds,"\nOld field id contain pk is = ", oldId)
    print("Different ? ", newIds != oldId)
    if newIds != oldId:
        query = 'ALTER TABLE ' + headerId + ' DROP CONSTRAINT '
        query += oldId
        query += ',\n' + 'ALTER TABLE ' + headerId + ' ADD CONSTRAINT ' + "PK_"+ newIds + ' PRIMARY KEY (' + newIds + ')'
        print("Returning = \n", query)   
    else:
        # query = 'Only copy form this >>'
        if len(oldField) != len(newField):
            query = 'detected More than '
            query += str(len(newField[len(oldField):len(newField)])) + ' new PK '
            newPks = newField[len(oldField):len(newField)]
            query += 'Added to ' + headerId  + "PK_"+ newField[0]['fieldName']['value'] + ' Please drop this table first and create again with view queries button !'

    return query
  
def detectStatTD(obj,headerId):
    emberQuery = []
    for el in obj['field']:
        if el['statTD'] == 'inactive':
            query = "Removing " + el['fieldName']['value'] + " " + el['datTypeField'].upper() + "(" + str(el['maxlenField']) + ")" + " From Table " + headerId
            emberQuery.append(query)
    
    return emberQuery

def generateIdHeader(obj):
    print(obj,'>>>???>>>')
    firstStr = obj['appName']['value']
   
    midStr = obj['isMaster']['key'][0]
    
    kategori = obj['isMaster']['value']
    appName = obj['appName']['text']
    
    result = firstStr + midStr
    
    
    if obj['joinTo'] and obj['joinTo'] != 'None':
        print(obj['joinTo'])
        a = obj['joinTo'][0:-1]
        b = int(obj['joinTo'][-1]) + 1
        result = a + str(b)
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
            if el['table_id'] == result:
                reGenerate = el['table_id'][0:-1] + str(int(el['table_id'][-1]) + 1)
                result = reGenerate
                return result
        return result
            
    else:
        cur_sql.execute("""
                        Select TOP 1
                            AAMTBIDZ1302 as table_id ,  
                            AAMCPTBZ1302 as caption_table,
                            AAMALIDZ1302 as aplication_id,
                            AAMALNMZ1302 as aplication_name,
                            AAMKTAPZ1302 as kategori_app
                        From AAMTBHAZ1301
                        Where AAMALNMZ1302 = '{appName}' and AAMKTAPZ1302 = '{kategori}'
                        ORDER by AAMTBIDZ1302 DESC
                        """.format(appName=appName,kategori=kategori))
        k = cur_sql.fetchone()
        if k:
            ids = k[0]
            if len(ids) <= 6:
                mid = int(ids[3:5]) + 10
                last = 1
                result += str(mid) + str(last)
                return result
            elif len(ids) <= 8:
                mid = int(ids[5:7]) + 10
                last = 1
                result += str(mid) + str(last)
                return result
        else:
            getMidNumb = str(10)
            getLastNumb = str(1)
        
        
        result += getMidNumb + getLastNumb
        # check duplicated 
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
        if checkData:
            for el in checkData:
                if el['table_id'] == result:
                    reGenerate = el['table_id'][0:-1] + str(int(el['table_id'][-1]) + 1)
                    result = reGenerate
                    return result
                else:
                    return result
        else:
            return result

def generateIdTDetail(input, headerId):
    isMaster = ''
    lastNumber = ''
    if len(headerId) == 6 :
        isMaster = headerId[2:4]
        lastNumber = headerId[4:7]
    elif len(headerId) == 8:
        isMaster = headerId[4:5]  
        lastNumber = headerId[5:8]
    
    result =  input + isMaster + lastNumber

    return result
 
def postQuery(obj):
    result = []
    header_id = generateIdHeader(obj)
    query1 = f"CREATE TABLE {header_id} ("

    field_ids = [generateIdTDetail(el['fieldName']['value'], header_id) for el in obj['field'] if el['isPk']]
    counter_pk = len(field_ids)
    last = f"CONSTRAINT PK_{header_id} PRIMARY KEY ({', '.join(field_ids)})"

    fields = [f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']}({el['maxlenField']})" for el in obj['field']]

    if counter_pk > 1:
        result = fields
        result.insert(0, query1)
        result.append(last)
        result.append(')')
        return "?".join(result)
    else:
        fieldss = [f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']}({el['maxlenField']}) {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" for el in obj['field']]
        result = fieldss
        result.insert(0, query1)
        result.append(')')
        return "?".join(result)
    
def editedPostQuery(obj):
    result = []
    header_id = generateIdHeader(obj)
    query1 = f"CREATE TABLE {header_id} ("

    field_ids = [generateIdTDetail(el['fieldNameEdit']['value'], header_id) for el in obj['field'] if el['isPk']]
    counter_pk = len(field_ids)
    last = f"CONSTRAINT PK_{header_id} PRIMARY KEY ({', '.join(field_ids)})"

    fields = [f"{generateIdTDetail(el['fieldNameEdit']['value'], header_id)} {el['datTypeField']}({el['maxlenField']})" for el in obj['field']]

    if counter_pk > 1:
        result = fields
        result.insert(0, query1)
        result.append(last)
        result.append(')')
        return "?".join(result)
    else:
        fieldss = [f"{generateIdTDetail(el['fieldNameEdit']['value'], header_id)} {el['datTypeField']}({el['maxlenField']}) {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" for el in obj['field']]
        result = fieldss
        result.insert(0, query1)
        result.append(')')
        return "?".join(result)
    
def postExtQuery(obj):
    print("==================== Generating Query ==========================")
    print("Generated = ")
    print(obj,"<<<<")
    result = []
    
    header_id = ''
    if obj['extTableName']:
        header_id = obj['extTableName'].upper()
    else:
        getTable = obj['tableName']
        cur_sql.execute("""
                            SELECT AAMTBIDZ1302 FROM AAMTBHAZ1301
                            WHERE AAMCPTBZ1302 = '{tana}'
                        """.format(tana = getTable))
        rows = cur_sql.fetchone()
        header_id = rows[0]
        
    query1 = f"CREATE TABLE {header_id} ("
    field_ids = []
    
    if obj['tableName'] == None:
        field_ids = [el['fieldName'] for el in obj['field'] if el['isPk']]
    else:
        field_ids = [el['fieldName']['value'] if el['fieldName']['value'] else el['fieldName'] for el in obj['field'] if el['isPk']]
    
        print(field_ids,">>>>>")
    counter_pk = len(field_ids)
    last = f"CONSTRAINT PK_{header_id} PRIMARY KEY ({', '.join(field_ids)})"

    fields = [f"{el['fieldName']} {el['datTypeField']}({el['maxlenField']})" for el in obj['field']]

    if counter_pk > 1:
        result = fields
        result.insert(0, query1)
        result.append(last)
        result.append(')')
        return "?".join(result)
    else:
        fieldss = [f"{el['fieldName']['value'] if isinstance(el['fieldName'], dict) else el['fieldName']} {el['datTypeField']}({el['maxlenField']}) {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" for el in obj['field']]
        result = fieldss
        result.insert(0, query1)
        result.append(')')
        return "?".join(result)

def editQuery(inputNew,id):
    cur_sql.execute("""
            SELECT
                AAMTBIDZ1302 as headerId,
                AAMQESRZ1302 as query_existing  
            from AAMTBHAZ1301
            where AAMTBIDZ1302 = %s
            """, (id,))
    result1 = [dict(zip([column[0] for column in cur_sql.description], [
                    str(x).strip() for x in row])) for row in cur_sql]


    cur_sql.execute("""
                SELECT 
                    AAMFEIDZ1302 as fieldId,
                    AAMHAIDZ1302 as headerId,
                    AAMVLZ1302 as defaultValue,
                    AAMDTZ1302 as dataType,
                    AAMPKZ1302 as isPk,
                    AAMSTTDZ1301 as 'statusTD'
                FROM AAMTBDTZ1301
                where AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
                """, (id,))
    result2 = [dict(zip([column[0] for column in cur_sql.description], [
                    str(x).strip() for x in row])) for row in cur_sql]

    old = {'table_data': result1, 'field_data': result2}
    
    editedCol = []
    for i in range(len(result2)):
        old_id = old['field_data'][i]['fieldId']
        header_id = old['field_data'][i]['headerId']
        
        if len(header_id) == 8:
            isMaster = header_id[4:5]  
            lastNumber = header_id[5:8]
        if len(header_id) == 6 :
            isMaster = header_id[2:4]
            lastNumber = header_id[4:7]
        getNewInputId =  generateIdTDetail(inputNew['field'][i]['fieldNameEdit']['value'], header_id)
        if old_id != getNewInputId:
            new_id = generateIdTDetail(inputNew['field'][i]['fieldNameEdit']['value'], header_id)
            result_rename = renameCol(header_id, old_id, new_id)
            editedCol.append(result_rename)
        else:
            new_id = generateIdTDetail(inputNew['field'][i]['fieldNameEdit']['value'], header_id)
        
        new_datType = inputNew['field'][i]['datTypeField']
        new_maxLen = inputNew['field'][i]['maxlenField']
        old_datType = old['field_data'][i]['dataType']
        old_maxLen = old['field_data'][i]['defaultValue']
        
        if new_datType.upper() != old_datType and str(new_maxLen).upper() != old_maxLen:     
            result_edit_datatype = editDaType(header_id, new_id, new_datType, str(new_maxLen))
            editedCol.append(result_edit_datatype)
        
        
        
    changePk = detectPkChange(inputNew, id)
    if changePk != '':
        editedCol.append(changePk)
    
    changeStatuses = detectStatTD(inputNew,id)
    if changeStatuses:
        # changeStatuses[0] += 'XXXX'
        # changeStatuses.append('XXXX')
        for i in changeStatuses:
            editedCol.append(i)
        # editedCol.append(changeStatuses)
    
    newInputLen = len(inputNew['field'])
    oldLen = len(result2)
    
    if oldLen != newInputLen:
        
        newFields = inputNew['field'][oldLen : newInputLen]
        # jika newFields len <= 1 newFields['field'][0]['fieldName]
        for y in newFields:
            newIds = generateIdTDetail(y['fieldNameEdit']['value'],id)
            newDat = y['datTypeField'].upper()
            newMaxVal = y['maxlenField']
            newQueries = "ALTER TABLE " + id + " ADD " + newIds + " " + newDat + "(" + str(newMaxVal) + ")"
            editedCol.append(newQueries)
            
            
    # print(editedCol)
    if editedCol:
        # editedCol.append("<<")
        hasil = "\n".join(editedCol)
    else:
        hasil = "No Change Detected!"
   
    print("hasil Edit Query:", hasil)
    return hasil

def editExtQuery(inputNew,id):
    cur_sql.execute("""
            SELECT
                AAMTBIDZ1302 as headerId,
                AAMQESRZ1302 as query_existing  
            from AAMTBHAZ1301
            where AAMTBIDZ1302 = %s
            """, (id,))
    result1 = [dict(zip([column[0] for column in cur_sql.description], [
                    str(x).strip() for x in row])) for row in cur_sql]


    cur_sql.execute("""
                SELECT 
                    AAMFEIDZ1302 as fieldId,
                    AAMHAIDZ1302 as headerId,
                    AAMVLZ1302 as defaultValue,
                    AAMDTZ1302 as dataType,
                    AAMPKZ1302 as isPk,
                    AAMSTTDZ1301 as 'status tabel'
                FROM AAMTBDTZ1301
                where AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
                """, (id,))
    result2 = [dict(zip([column[0] for column in cur_sql.description], [
                    str(x).strip() for x in row])) for row in cur_sql]

    old = {'table_data': result1, 'field_data': result2}

    
    editedCol = []
    print(len(inputNew['field']),len(old['field_data']))
    for i in range(len(result2)):
        old_id = old['field_data'][i]['fieldId']
        header_id = old['field_data'][i]['headerId']

        if len(header_id) == 8:
            isMaster = header_id[4:5]  
            lastNumber = header_id[5:8]
        if len(header_id) == 6 :
            isMaster = header_id[2:4]
            lastNumber = header_id[4:7]
        getNewInputId =  inputNew['field'][i]['fieldName']['value']
        if old_id != getNewInputId:
            new_id = inputNew['field'][i]['fieldName']['value']
            result_rename = renameCol(header_id, old_id, new_id)
            editedCol.append(result_rename)
        else:
            new_id = inputNew['field'][i]['fieldName']['value']

        new_datType = inputNew['field'][i]['datTypeField']
        new_maxLen = inputNew['field'][i]['maxlenField']
        old_datType = old['field_data'][i]['dataType']
        old_maxLen = old['field_data'][i]['defaultValue']

        if new_datType.upper() != old_datType and str(new_maxLen).upper() != old_maxLen:     
            result_edit_datatype = editDaType(header_id, new_id, new_datType, str(new_maxLen))
            editedCol.append(result_edit_datatype)
        
        
        

    
    newInputLen = len(inputNew['field'])
    oldLen = len(result2)
    
    if oldLen < newInputLen:
        newFields = inputNew['field'][oldLen : newInputLen]
        # jika newFields len <= 1 newFields['field'][0]['fieldName]
        for y in newFields:
            print(newFields,';;;;;lskdkajsjdja;;;;;')
            newIds = y['fieldName'].upper()
            newDat = y['datTypeField'].upper()
            newMaxVal = y['maxlenField']
            newQueries = "ALTER TABLE " + id + " ADD " + newIds + " " + newDat + "(" + str(newMaxVal) + ")"
            editedCol.append(newQueries)
            
            
    changePk = detectPkChange(inputNew, id)
    if changePk != '':
        editedCol.append(changePk)
        
    changeStatuses = detectStatTD(inputNew,id)
    if changeStatuses:
        for i in changeStatuses:
            editedCol.append(i)
            
    if editedCol:
        # editedCol.append("<<")
        hasil = "\n".join(editedCol)
    else:
        hasil = "No Change Detected!"
   
    print("hasil Edit Existing Query:", hasil)
    return hasil

def getFieldsPerTable(obj):
    hasil = []
    for i in obj:
       ids = i['id']
       cur_sql.execute("""
                    SELECT 
                        COUNT(*) AS totalData
                    FROM AAMTBDTZ1301 WHERE AAMHAIDZ1302 = %s AND AAMSTTDZ1301 = 'active'
                """,(ids,))
       totalFields = cur_sql.fetchone()[0]
       data = {
           "headerId": ids,
           "totalField": totalFields
       }
       hasil.append(data)
       
    return hasil      