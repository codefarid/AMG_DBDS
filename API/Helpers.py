from DB import *
import re

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
    result = 'ALTER TABLE ' + headerId + ' RENAME ' + oldId + ' TO ' + newId
    return result

def editDaType(headerId, fieldId, datType, defVal):
    result = 'ALTER TABLE ' + headerId + ' ALTER COLUMN ' + fieldId + ' ' + datType + '(' + defVal + ')'
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
    newIds = newId['value']
    if newIds != oldId:
        query = 'ALTER TABLE ' + headerId + ' DROP CONSTRAINT '
        query += oldId
        query += ',\n' + 'ALTER TABLE ' + headerId + ' ADD CONSTRAINT ' + "PK_"+ newIds + ' PRIMARY KEY (' + newIds + ')'
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

def getTableNameFromDB(first,second):
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
                    order by TABLE_NAME ASC
                    """)
    t = []
    for row in cur_sql:
        t.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
    # print(t,len(t))
    storeList = []    
    for i in t:
        if first + second in i["TABLE_NAME"]:
            storeList.append(i["TABLE_NAME"])
            # print(i["TABLE_NAME"]," >  YHES!!")
    if len(storeList) > 0:
        # print(storeList)
        def extract_number(s):
            return int(re.search(r'\d+',s).group())
        def get_number_only(s):
            return int(''.join(filter(str.isdigit,s)))
        
        hasil = max(storeList, key=lambda x:(x.startswith(f'{first}{second}') and x[len(f'{first}{second}'):].isdigit(),extract_number(x)))
        number_aja = get_number_only(hasil) 
        return hasil , number_aja
    else:
        return None
    
def getTableNameFromInternal(first,second):
    cur_sql.execute("""
                    use TestAMGAPPS
                    select AAMTBIDZ1302 as 'TABLE_NAME' from AAMTBHAZ1301
                    where AAMTHSTZ1302 = 'active'
                    """)
    t = []
    for row in cur_sql:
        t.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
    storeList = []    
    for i in t:
        if first + second in i["TABLE_NAME"]:
            storeList.append(i["TABLE_NAME"])
    if len(storeList) > 0:
        def extract_number(s):
            return int(re.search(r'\d+',s).group())
        def get_number_only(s):
            return int(''.join(filter(str.isdigit,s)))
        hasil = max(storeList, key=lambda x:(x.startswith(f'{first}{second}') and x[len(f'{first}{second}'):].isdigit(),extract_number(x)))
        number_aja = get_number_only(hasil) 
        return hasil , number_aja
    else:
        return None

def generateIdHeader(obj):
    firstStr = obj['appName']['value']
    midStr = obj['isMaster']['key'][0]
    
    higestValueFromDB = getTableNameFromDB(firstStr,midStr)
    higestValueFromInternal = getTableNameFromInternal(firstStr,midStr)
    
    a = higestValueFromDB[1] if higestValueFromDB != None else 0
    b = higestValueFromInternal[1] if higestValueFromInternal != None else 0
    
        
    if obj['joinTo'] and obj['joinTo'] != None:
        def get_number_only(s):
            return int(''.join(filter(str.isdigit,s)))
        getNumber = get_number_only(obj['joinTo'])
        return f'{firstStr}{midStr}{getNumber + 1}'
    else:
        selectedHeaderId = ''
        if a > b:
            selectedHeaderId = higestValueFromDB[0]
        elif a < b:
            selectedHeaderId = higestValueFromInternal[0]
        else:
            selectedHeaderId = higestValueFromDB[0]            
            
        def get_number_only(s):
            return int(''.join(filter(str.isdigit,s)))
        val = get_number_only(selectedHeaderId[:-2])
        

        return f'{firstStr}{midStr}{val + 1}01'

def generateIdTDetail(input, headerId):
    temp1 = ""
    temp2 = ""
    temp4 = ""
    for i in range(len(headerId)):
        if i < 4:
            temp1 += headerId[i]
        elif i < 5:
            temp4 += headerId[i]
        else:
            temp2 += headerId[i]
    temp3 = [temp1, temp4, temp2]
    result = f"{input}{temp3[1]}{temp3[2]}"
    # print(result,'>>>>>>')
    return result
 
def postQuery(obj):
    result = []
    header_id = generateIdHeader(obj)
    query1 = f"CREATE TABLE {header_id} ("
    # print(header_id)
    field_ids = [generateIdTDetail(el['fieldName']['value'], header_id) for el in obj['field'] if el['isPk']]
    counter_pk = len(field_ids)
    last = f"CONSTRAINT PK_{header_id} PRIMARY KEY ({', '.join(field_ids)})"
    # print(field_ids)
    fields = [f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']}" if el['maxlenField'] == 0 else f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']}({el['maxlenField']})" for el in obj['field']]
    getFK = []
    for i in obj['field']:
        if i['isFK'] != '':
            getFK.append(f"CONSTRAINT FK_{generateIdTDetail(i['fieldName']['value'], header_id)} FOREIGN KEY ({generateIdTDetail(i['fieldName']['value'], header_id)}) REFERENCES {i['isFKto']}({i['isFK']})")

    if counter_pk > 1:
        result = fields
        result.insert(0, query1)
        result.append(last)
        if len(getFK) != 0:
            for y in getFK:
                result.append(y)
        result.append(')')
        return "?".join(result)
    else:
        fieldss = [f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']} {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" if el['maxlenField'] == 0 else f"{generateIdTDetail(el['fieldName']['value'], header_id)} {el['datTypeField']}({el['maxlenField']}) {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" for el in obj['field']]
        result = fieldss
        result.insert(0, query1)
        if len(getFK) != 0:
            for y in getFK:
                result.append(y)
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
        result.append(');')
        return "?".join(result)
    else:
        fieldss = [f"{generateIdTDetail(el['fieldNameEdit']['value'], header_id)} {el['datTypeField']}({el['maxlenField']}) {'NOT NULL PRIMARY KEY' if el['isPk'] else ''}" for el in obj['field']]
        result = fieldss
        result.insert(0, query1)
        result.append(');')
        return "?".join(result)
    
def postExtQuery(obj):
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
                    AAMSTTDZ1301 as 'statusTD',
                    AAMISFKZ1301 as 'isFK',
                    AAMFKTOZ1301 as 'isFKto'
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
        new_isFk = inputNew['field'][i]['isFK']['value']
        old_isFK = old['field_data'][i]['isFK']
        new_isFKto = inputNew['field'][i]['isFKto']['value']
        old_isFKto = old['field_data'][i]['isFKto']
        
        if new_datType.upper() != old_datType and str(new_maxLen).upper() != old_maxLen:     
            result_edit_datatype = editDaType(header_id, new_id, new_datType, str(new_maxLen))
            editedCol.append(result_edit_datatype)
        
        if new_isFk != '' and new_isFKto != '':    
            if new_isFk != old_isFK and new_isFKto != old_isFKto:
                editedCol.append(f'ALTER TABLE {header_id} ADD CONSTRAINT FK_{header_id}_{new_isFKto} FOREIGN KEY ({old_id}) REFERENCES {new_isFKto}({new_isFk})')
        
        
        
        
        
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
            newIsFK = y['isFK']["value"] if y['isFK']["value"] != '' else '0'
            newIsFKto = y['isFKto']["value"] if y['isFKto']["value"] != '' else '0'
            newQueries = "ALTER TABLE " + id + " ADD " + newIds + " " + newDat + "(" + str(newMaxVal) + ")"
            
            editedCol.append(newQueries)
            if newIsFK != '0' and newIsFKto != '0':
                editedCol.append(f'ALTER TABLE {header_id} ADD CONSTRAINT FK_{header_id}_{new_isFKto} FOREIGN KEY ({newIds}) REFERENCES {newIsFKto}({newIsFK})')
            
            
    # print(editedCol)
    if editedCol:
        # editedCol.append("<<")
        hasil = "\n".join(editedCol)
    else:
        hasil = "No Change Detected!"
   
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