from DB import *
import os
import json
import pprint
import re

from collections import defaultdict
# from Helpers import *

data = {
    "tableName": "sss",
    "extTableName": None,
    "isMaster": {
        "key": "Transaction",
        "status": "active",
        "value": "2"
    },
    "extName": None,
    "appName": {
        "text": "EXIM SYSTEM",
        "value": "AA"
    },
    "joinTo": "",
    "status": None,
    "isExisted": None,
    "field": [
        {
            "fieldNameEdit": "",
            "extFname": "",
            "fieldName": {
                "key": "Valuta",
                "status": "active",
                "value": "VALT"
            },
            "datTypeField": "varchar",
            "maxlenField": 50,
            "isPk": True,
            "isFK": "",
            "isFKto": "",
            "statTD": "active"
        }
    ]
}

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
        print(getNumber + 1)
        return f'{firstStr}{midStr}{getNumber + 1}'
    else:
        lastStr = 0
        if a > b:
            lastStr = a
        elif a < b:
            lastStr = b
        else:
            lastStr = a
        return f'{firstStr}{midStr}{lastStr + 101}'
        
    
   
print(generateIdHeader(data))

# ow = "EXIMT901"

# if "EXIM" in ow:
#     print("YHES")