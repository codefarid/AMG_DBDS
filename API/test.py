from DB import *
import os
import json
import pprint

from collections import defaultdict
from Helpers import *



# dataSB = [{
#             "key": '0',
#             "label": 'Document Purchase 2',
#             "data": 'DOMSM201',
#             "icon": 'pi pi-fw pi-table',
#             "children": [
#                 {
#                     "key": '0-0',
#                     "label": 'Field Key',
#                     "data": 'DFFKM201',
#                     "icon": 'pi pi-fw pi-server'
#                 },
#                 {
#                     "key": '0-1',
#                     "label": 'Home',
#                     "data": 'QCDTM201',
#                     "icon": 'pi pi-fw pi-server'
#                 }
#             ]
#         },
#           ]

# cur_sql.execute("""
#                 SELECT    
#                 AAMTBHAZ1301.AAMTBIDZ1302 AS table_id,
#                 AAMTBHAZ1301.AAMCPTBZ1302 AS caption_table,
#                 AAMTBHAZ1301.AAMALNMZ1302 AS aplication_name,
#                 AAMTBDTZ1301.AAMFEIDZ1302 AS field_id,
#                 AAMTBDTZ1301.AAMNMZ1302 AS name_caption
#                 FROM
#                 AAMTBHAZ1301
#                 INNER JOIN 
#                 AAMTBDTZ1301 ON AAMTBHAZ1301.AAMTBIDZ1302 = AAMTBDTZ1301.AAMHAIDZ1302
#                 where AAMTHSTZ1302 = 'active';
#                 """)
# rawData = []
# for row in cur_sql:
#     rawData.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
# counter = 0
# counter2= 0
# dataSB = []
# for el in rawData:
#     existingItem = next((item for item in dataSB if item["data"] == el["table_id"] and item["label"] == el["caption_table"]), None)
#     # print(existingItem)
#     if existingItem:
#         counter2 += 1
#         secNum = int(existingItem["children"][-1]["key"].split("-")[1])
#         existingItem['children'].append({
#                     "key": f'{existingItem["key"]}-{secNum + 1}',
#                     "label": el['name_caption'],
#                     "data": el['field_id'],
#                     "icon": 'pi pi-fw pi-server'
#                 })
#     else:
#         counter2 += 1
#         dataSB.append({
#             "key": f'{counter}',
#             "label": el['caption_table'],
#             "data": el['table_id'],
#             "icon": 'pi pi-fw pi-table',
#             "app": el['aplication_name'],
#             "children": [{
#                     "key": f'{counter}-{0}',
#                     "label": el['name_caption'],
#                     "data": el['field_id'],
#                     "icon": 'pi pi-fw pi-server'
#                 }]})
#         # counter2 = 0
#     counter += 1
#     counter2 = 0

# pprint.pprint(dataSB)
# b1 = [
#     {'document_id': '600006519', 'posting_date': '08/09/2023', 'nama_barang': 'CSB LOR SIZE 610x47.5x85', 'user': 'santoso', 'status': '1'},
#     {'document_id': '600006521', 'posting_date': '08/09/2023', 'nama_barang': 'PLYWOOD BACK SIDE 15 MM 520X1000 MM', 'user': 'santoso', 'status': '1'},
#     {'document_id': '600006519', 'posting_date': '08/09/2023', 'nama_barang': 'PLYWOOD BOTTOM SIDE 15 MM 710X850 MM', 'user': 'santoso', 'status': '1'},
#     {'document_id': '600006522', 'posting_date': '09/09/2023', 'nama_barang': 'ACSB LOR SIZE 610x47.5x85', 'user': 'santoso', 'status': '1'},
#     {'document_id': '600006523', 'posting_date': '09/09/2023', 'nama_barang': 'APLYWOOD BACK SIDE 15 MM 520X1000 MM', 'user': 'santoso', 'status': '1'},
#     {'document_id': '600006522', 'posting_date': '09/09/2023', 'nama_barang': 'APLYWOOD BOTTOM SIDE 15 MM 710X850 MM', 'user': 'santoso', 'status': '1'}
# ]

# # result = [
# #     {   
# #         'posting_date': '08/09/2023',
# #         "document_id": "600006519",
# #         "item_name": [
# #             "CSB LOR SIZE 610x47.5x85",
# #             "PLYWOOD BOTTOM SIDE 15 MM 710X850 MM"
# #         ], 
# #         'user': 'santoso', 
# #         'status': '1'
# #     },
# #     {   
# #         'posting_date': '08/09/2023',
# #         "document_id": "600006521",
# #         "item_name": [
# #             "PLYWOOD BACK SIDE 15 MM 520X1000 MM"
# #         ], 
# #         'user': 'santoso', 
# #         'status': '1'
# #     },
# #     {   
# #         'posting_date': '09/09/2023',
# #         "document_id": "600006525",
# #         "item_name": [
# #             "SP - Catridge filter 10 in 1 micron/Z92",
# #             "PLYWOOD BOTTOM SIDE 15 MM 520X1000 MM"
# #         ], 
# #         'user': 'santoso', 
# #         'status': '1'
# #     },
# #     {   
# #         'posting_date': '09/09/2023',
# #         "document_id": "600006523",
# #         "item_name": [
# #             "TISSUE ROL NICE/Z92",
# #             "Mouse"
# #         ], 
# #         'user': 'santoso', 
# #         'status': '1'
# #     }
# # ]
# result = []
# for el in b1:
#     existingItem = next((item for item in result if item["posting_date"] == el["posting_date"] and item["user"] == el["user"] and item["status"] == el["status"]), None)
#     # print(existingItem)
#     if existingItem:
#         existingDocument = next((doc for doc in existingItem["items"] if doc["document_id"] == el["document_id"]), None)
#         if existingDocument:
#             existingDocument["item_name"].append(el["nama_barang"])
#         else:
#             existingItem["items"].append({
#                 "document_id": el["document_id"],
#                 "item_name": [el["nama_barang"]],
#             })
#     else:
#         result.append({
#             "posting_date": el["posting_date"],
#             "user": el["user"],
#             "status": el["status"],
#             "items": [
#                 {
#                     "document_id": el["document_id"],
#                     "item_name": [el["nama_barang"]],
#                 }
#             ],
#         })

# # pprint.pprint(result)
# # print(rawData)
# [{
#     'table_id': 'DOMSM201',
#     'caption_table': 'Document Purchase 2', 
#     'field_id': 'DFFKM201', 
#     'header_id': 'DOMSM201', 
#     'name_caption': 'Field Key'
#     }, 
#  {
#      'table_id': 'DOMSM201',
#      'caption_table': 'Document Purchase 2',
#      'field_id': 'QCDTM201', 
#      'header_id': 'DOMSM201', 
#      'name_caption': 'Quality Control Date'
#      },
#  {
#      'table_id': 'DOMSM202', 
#      'caption_table': 'Purchase Document',
#      'field_id': 'DCNAM202', 
#      'header_id': 'DOMSM202',
#      'name_caption': 'Document Name'
#      }, 
#  {
#      'table_id': 'DOMSM202',
#      'caption_table': 'Purchase Document', 
#      'field_id': 'PDNAM201', 
#      'header_id': 'DOMSM202',
#      'name_caption': 'Purchase Discount Name'
#      }, 
#  {
#      'table_id': 'DOMSM202',
#      'caption_table': 'Purchase Document',
#      'field_id': 'PRDNM202', 
#      'header_id': 'DOMSM202',
#      'name_caption': 'Purchase Request No'
#      }, 
#  {
#      'table_id': 'DOMSM401',
#      'caption_table': 'Document Purchase 2',
#      'field_id': 'DFFKM401',
#      'header_id': 'DOMSM401',
#      'name_caption': 'Field Key'
#      }, 
#  {
#      'table_id': 'DOMSM401',
#      'caption_table': 'Document Purchase 2',
#      'field_id': 'QCDTM401',
#      'header_id': 'DOMSM401',
#      'name_caption': 'Quality Control Date'
#      }, 
#  {
#      'table_id': 'EXIMM101',
#      'caption_table': 'Exim',
#      'field_id': 'CAPTM101',
#      'header_id': 'EXIMM101',
#      'name_caption': 'Calibration Periode Type'
#     }, 
#  {
#      'table_id': 'EXIMM101',
#      'caption_table': 'Exim', 
#      'field_id': 'DCCOM101',
#      'header_id': 'EXIMM101',
#      'name_caption': 'Document Code'
#      }, 
#  {
#      'table_id': 'EXIMM101',
#      'caption_table': 'Exim',
#      'field_id': 'NAMEM101',
#      'header_id': 'EXIMM101',
#      'name_caption': 'Name'
#      }] 

a = "EXIMT1001"
b = "EXIMT101"

# def generatedFieldId(string,header_id):
#     temp1 = ""
#     temp2 = ""
#     temp4 = ""
#     for i in range(len(header_id)):
#         if i < 4:
#             temp1 += header_id[i]
#         elif i < 5:
#             temp4 += header_id[i]
#         else:
#             temp2 += header_id[i]
#     temp3 = [temp1, temp4, temp2]
#     result = f"{string}{temp3[1]}{temp3[2]}"
#     return result
# print(generatedFieldId("NOPEN",a))
# print(generateIdTDetail("IDNO", a))

ids = "EXIMT1001"
a = ''
b = ''
c = ''
for i in range(len(ids)):
    if i < 4:
        a += ids[i]
    elif i < 5:
        b += ids[i]
    else:
        c += ids[i]
if int(c) > 1000:
    c = int(c) + 100
print(a,b,c)