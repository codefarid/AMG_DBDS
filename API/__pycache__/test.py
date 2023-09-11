from DB import *
from Helpers import *

# obj = {
#     "tableName": "Master Aplication A",
#     "extTableName": None,
#     "isMaster": {
#         "key": "Master",
#         "status": "active",
#         "value": "1"
#     },
#     "extName": None,
#     "appName": {
#         "text": "Home Apps",
#         "value": "AA"
#     },
#     "joinTo": "AAM101",
#     "status": None,
#     "field": [
#         {
#             "extFname": "",
#             "fieldName": {
#                 "key": "Available Status",
#                 "status": "active",
#                 "value": "AAST"
#             },
#             "datTypeField": "varchar",
#             "maxlenField": 123,
#             "isPk": True
#         }
#     ]
# }
# # print(generateIdHeader(obj))

# cur_sql.execute("""
#                 SELECT AAMTBIDZ1302 as ids
#                 From AAMTBHAZ1301
#                 """)
# checkData = []
# for row in cur_sql:
#     checkData.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

# print(checkData)

data = {
    "tableName": "Aplication Master A",
    "extTableName": "",
    "isMaster": {
        "key": "Master",
        "status": "active",
        "value": "1"
    },
    "extName": "",
    "appName": {
        "text": "Home Apps",
        "value": "AA"
    },
    "joinTo": "None",
    "status": "active",
    "isExisted": "0",
    "field": [
        {
            "fieldNameEdit": {
                "key": "Available Quantity",
                "status": "active",
                "value": "AAQT"
            },
            "extFname": "Available Quantity",
            "fieldName": {
                "value": "AAQTM101"
            },
            "maxlenField": 123,
            "datTypeField": "varchar",
            "isPk": False,
            "statTD": "inactive"
        },
        {
            "fieldNameEdit": {
                "key": "Category Name",
                "status": "active",
                "value": "CANA"
            },
            "extFname": "Category Name",
            "fieldName": {
                "value": "CANAM101"
            },
            "maxlenField": 123,
            "datTypeField": "varchar",
            "isPk": False,
            "statTD": "inactive"
        },
        {
            "fieldNameEdit": {
                "key": "Calibration Periode Type",
                "status": "active",
                "value": "CAPT"
            },
            "extFname": "Calibration Periode Type",
            "fieldName": {
                "value": "CAPTM101"
            },
            "maxlenField": 123,
            "datTypeField": "varchar",
            "isPk": False,
            "statTD": "inactive"
        },
        {
            "fieldNameEdit": {
                "key": "Variable Value",
                "status": "active",
                "value": "VALU"
            },
            "extFname": "Variable Value",
            "fieldName": {
                "value": "VALUM101"
            },
            "maxlenField": 123,
            "datTypeField": "varchar",
            "isPk": True,
            "statTD": "active"
        },
        {
            "fieldNameEdit": {
                "key": "Variable Name",
                "status": "active",
                "value": "VANA"
            },
            "extFname": "Variable Name",
            "fieldName": {
                "value": "VANAM101"
            },
            "maxlenField": 123,
            "datTypeField": "varchar",
            "isPk": False,
            "statTD": "active"
        }
    ]
}


filterDatas = {}
# for o in data:
#     filterDatas['tableName'] = o['tableName']
#     filterDatas['extTableName'] = o['extTableName']
#     filterDatas['isMaster'] = o['isMaster']
#     filterDatas['extName'] = o['extName']
#     filterDatas['appName'] = o['appName']
#     filterDatas['joinTo'] = o['joinTo']
#     filterDatas['status'] = o['status']
#     filterDatas['isExisted'] = o['isExisted']

filte = {}

for i in data:
    if i != i['field']:
        filte = i
        
    
    
print(filterDatas)
print(filte)
