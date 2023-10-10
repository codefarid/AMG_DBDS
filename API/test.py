from DB import *
import os
import json
import pprint
import re

# print("MIGRATING TABLE HEADER DATA >>>")

# cur_sql.execute("""
#                 Select 
#                     AAMTBIDZ1302 as tbid,
#                     AAMCPTBZ1302 as capt,
#                     AAMALIDZ1302 as apid,
#                     AAMALNMZ1302 as apna, 
#                     AAMKTAPZ1302 as kate,
#                     AAMQESRZ1302 as qs,
#                     AAMTHSTZ1302 as stat,
#                     AAMJOINZ1302 as joinTo,
#                     AAMTHISZ1301 as history,
#                     AAMEXTTZ1301 as existing,
#                     AAMCEATZ1302 as crdt,
#                     AAMCETMZ1302 as crtm,
#                     AAMCEUEZ1302 as crus,
#                     AAMUDATZ1302 as updt,
#                     AAMUDTMZ1302 as uptm,
#                     AAMUDUEZ1302 as upus
#                 from AAMTBHAZ1301
#                 """)

# header = []
# for row in cur_sql:
#     header.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
# print("SENT DATA HEADER >>>")

# countHeader = 0
# for i in header:    
#     cur_sql.execute("""
#                     INSERT INTO AAM1701 (TBIDM1701,CPTBM1701,APNOM1701,APNAM1701,KTAPM1701,QESRM1701,STATM1701,JOINM1701,HISTM1701,EXTTM1701,CRDTM1701,CRTMM1701,CRUSM1701,UPDTM1701,UPTIM1701,UPUSM1701)
#                     VALUES ('{tbid}','{capt}','{apid}','{apna}','{kate}','{qs}','{stat}','{joinTo}','{history}','{existing}','{crdt}','{crtm}','{crus}','{updt}','{uptm}','{upus}')
#                     """.format(
#                             tbid = i["tbid"],
#                             capt = i["capt"],
#                             apid = i["apid"],
#                             apna = i["apna"],
#                             kate = i["kate"],
#                             qs = i["qs"],
#                             stat = i["stat"],
#                             joinTo = i["joinTo"],
#                             history = i["history"],
#                             existing = i["existing"],
#                             crdt = i["crdt"],
#                             crtm = i["crtm"],
#                             crus = i["crus"],
#                             updt = i["updt"],
#                             uptm = i["uptm"],
#                             upus = i["upus"]
#                     ))
#     DB_SQL.commit()
#     countHeader += 1
#     print("Header Data SENT : ", countHeader)
    
    


# print("MIGRATING TABLE DETAIL >>>")
# cur_sql.execute("""
#                 Select 
#                     AAMFEIDZ1302 as fid,
#                     AAMHAIDZ1302 as hid,
#                     AAMDTZ1302 as dt,
#                     AAMNMZ1302 as nc,
#                     AAMVLZ1302 as dv,
#                     AAMEXTDZ1301 as existing,
#                     AAMISFKZ1301 as isfk,
#                     AAMFKTOZ1301 as fkto,
#                     AAMPKZ1302 as pk,
#                     AAMSTTDZ1301 as stat,
#                     AAMCEATZ1302 as crdt,
#                     AAMCETMZ1302 as crtm,
#                     AAMCEUEZ1302 as crus,
#                     AAMUDATZ1302 as updt,
#                     AAMUDTMZ1302 as uptm,
#                     AAMUDUEZ1302 as upus 
#                 from AAMTBDTZ1301
#                 """)
# detail = []
# for row in cur_sql:
#             detail.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

# countDetail = 0
# for i in detail:
#     cur_sql.execute("""
#                     INSERT INTO AA (
#                         FEID,
#                         HEID,
#                         DATY,
#                         NMCA,
#                         DEVA,
#                         EXTD,
#                         ISFK,
#                         FKTO,
#                         ISPK,
#                         STAT,
#                         CRDT,
#                         CRTM,
#                         CRUS,
#                         UPDT,
#                         UPTI,
#                         UPUS
#                         )
#                     VALUES ('{fid}','{hid}','{dt}','{nc}','{dv}','{existing}','{isfk}','{fkto}','{pk}','{stat}','{crdt}','{crtm}','{crus}','{updt}','{uptm}','{upus}')
#                     """.format(
#                         fid = i['fid'],
#                         hid = i['hid'],
#                         dt = i['dt'],
#                         nc = i['nc'],
#                         dv = i['dv'],
#                         existing = i['existing'],
#                         isfk = i['isfk'],
#                         fkto = i['fkto'],
#                         pk = i['pk'],
#                         stat = i['stat'],
#                         crdt = i['crdt'],
#                         crtm = i['crtm'],
#                         crus = i['crus'],
#                         updt = i['updt'],
#                         uptm = i['uptm'],
#                         upus = i['upus'] 
#                     ))
#     DB_SQL.commit()
#     countDetail += 1
#     print("Detail Data Sent : ", countDetail)
    
# print("MIGRATING TABLE DEFINITION >>>")

# cur_sql.execute("""
#                 SELECT
#                     AAMTBCOZ1302 as tbcode,
#                     AAMTDEFZ1302 as tbdef,
#                     AAMDSTAZ1302 as stat,
#                     AAMDADEZ1302 as crdt,
#                     AAMTIDEZ1302 as cdtm,
#                     AAMCUDEZ1302 as crus,
#                     AAMUDDEZ1302 as updt,
#                     AAMUTDEZ1302 as uptm,
#                     AAMUUDEZ1302 as upus
#                 FROM AAMTBDEZ1301
#                 """)
# definition = []
# for row in cur_sql:
#             definition.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

# countDefinition = 0
# for i in definition:
#     cur_sql.execute("""
#                     INSERT INTO AAM1501 ( TBNOM1501, TBDEM1501,STATM1501,CRDTM1501,CRTMM1501,CRUSM1501,UPDTM1501,UPTIM1501,UPUSM1501)
#                     VALUES ('{tbcode}','{tbdef}','{stat}','{crdt}','{cdtm}','{crus}','{updt}','{uptm}','{upus}')
#                     """.format(
#                         tbcode = i['tbcode'],
#                         tbdef = i['tbdef'],
#                         stat = i['stat'],
#                         crdt = i['crdt'],
#                         cdtm = i['cdtm'],
#                         crus = i['crus'],
#                         updt = i['updt'],
#                         uptm = i['uptm'],
#                         upus = i['upus']
#                     ))
#     DB_SQL.commit()
#     countDefinition += 1
#     print("Definition Data Sent : ", countDefinition)

# print("MIGRATING TABLE CATEGORIES")

# cur_sql.execute("""
#                 SELECT
#                     AAMCAVAZ1302 as val,
#                     AAMCKEYZ1302 as 'key',
#                     AAMCSTAZ1302 as stat,
#                     AAMDACAZ1302 as crdt,
#                     AAMTACAZ1302 as crti,
#                     AAMUSCAZ1302 as crus,
#                     AAMUDACZ1302 as updt,
#                     AAMUTACZ1302 as uptm,
#                     AAMUUSCZ1302 as upus
#                 FROM AAMTCATEZ1301
#                 """)

# categories = []
# for row in cur_sql:
#             categories.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))

# countCategories = 0
# for i in categories:
#     cur_sql.execute("""
#                     INSERT INTO AAM1601 (CANOM1601,CANAM1601,STATM1601,CRDTM1601,CRTMM1601,CRUSM1601,UPDTM1601,UPTIM1601,UPUSM1601)
#                     VALUES ('{val}','{key}','{stat}','{crdt}','{crti}','{crus}','{updt}','{uptm}','{upus}')
#                     """.format(
#                         val = i['val'],
#                         key = i['key'],
#                         stat = i['stat'],
#                         crdt = i['crdt'],
#                         crti = i['crti'],
#                         crus = i['crus'],
#                         updt = i['updt'],
#                         uptm = i['uptm'],
#                         upus = i['upus']
#                     ))
#     DB_SQL.commit()
#     countCategories += 1
#     print("SENT CATEGORIES DATA : " , countCategories)
    

"""
SELECT
ROIDM1101 as 'Row ID',
APCDM1101 as 'App Code',
MOCDM1101 as 'Module Code',
MRNAM1101 as 'Master Name',
TSTPM1101 as 'Time Stamp',
CRUSM1101 as 'create user',
UPDTM1101 as 'Update Date',
UPTIM1101 as 'Update Time',
UPUSM1101 as 'Update User'
from AAM1101

CREATE TABLE AAM1101 (
ROIDM1101 VARCHAR(50) NOT NULL PRIMARY KEY,
APCDM1101 VARHAR(20),
MOCDM1101 VARHAR(20),
MRNAM1101 VARHAR(100),
TSTPM1101 VARHAR(20),
CRUSM1101 VARHAR(20),
UPDTM1101 VARHAR(20),
UPTIM1101 VARHAR(20),
UPUSM1101 VARHAR(20)
)

select
ROIDM1102 as 'Row ID',
ITNOM1102 as 'Item Code',
DESCM1102 as 'Description',
IDKSM1102 as 'ID Export',
IDIMM1102 as 'ID Import',
IDMCM1102 as 'IDOMA Code',
TSTPM1102 as 'Time Stamp',
CRUSM1102 as 'Create User',
UPDTM1102 as 'Update Date',
UPTIM1102 as 'Update Time',
UPUSM1102 as 'Update User'
from AAM1102

CREATE TABLE AAM1102 (?
ROIDM1102  VARCHAR(50) NOT NULL PRIMARY KEY,?
ITNOM1102  VARCHAR(20) NOT NULL PRIMARY KEY,?
DESCM1102  VARCHAR(225),?
IDKSM1102  VARCHAR(20),?
IDIMM1102  VARCHAR(20),?
IDMCM1102  VARCHAR(20),?
TSTPM1102  VARCHAR(20),?
CRUSM1102  VARCHAR(20),?
UPDTM1102  VARCHAR(20),?
UPTIM1102  VARCHAR(20),?
UPUSM1102  VARCHAR(20),?
CONSTRAINT PK_AAM1102 PRIMARY KEY (ROIDM1102, ITNOM1102))?
)

"""

# TABLE HEADER 1101
tbha101 = [
    {
        'TBID': 'AAM1101',
        'CPTB': 'AAM1101',
        'APNO': '2022-07-APPCT-0001', 
        'APNA': 'Home Apps',
        'KTAP': '1', 
        'QESR': 'CREATE TABLE AAM1101 (?ROIDM1101 VARCHAR(50) NOT NULL PRIMARY KEY,?APCDM1101 VARHAR(20),?MOCDM1101 VARHAR(20),?MRNAM1101 VARHAR(100),?TSTPM1101 VARHAR(20),?CRUSM1101 VARHAR(20),?UPDTM1101 VARHAR(20),?UPTIM1101 VARHAR(20),?UPUSM1101 VARHAR(20)?)',
        'STAT': 'active', 
        'JOIN': 'None', 
        'HIST': 'None',
        'EXTT': '0', 
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },{
        'APNA': 'Home Apps',
        'APNO': '2022-07-APPCT-0001', 
        'CPTB': 'AAM1102',
        'CRDT': '20230919',
        'CRTM': '1423',
        'CRUS': 'farid.farid',
        'EXTT': '0', 
        'HIST': 'None',
        'JOIN': 'None', 
        'KTAP': '1', 
        'QESR': 'CREATE TABLE AAM1102 (?ROIDM1102  VARCHAR(50) NOT NULL PRIMARY KEY,?ITNOM1102  VARCHAR(20) NOT NULL PRIMARY KEY,?DESCM1102  VARCHAR(225),?IDKSM1102  VARCHAR(20),?IDIMM1102  VARCHAR(20),?IDMCM1102  VARCHAR(20),?TSTPM1102  VARCHAR(20),?CRUSM1102  VARCHAR(20),?UPDTM1102  VARCHAR(20),?UPTIM1102  VARCHAR(20),?UPUSM1102  VARCHAR(20),?CONSTRAINT PK_AAM1102 PRIMARY KEY (ROIDM1102, ITNOM1102))?)',
        'STAT': 'active', 
        'TBID': 'AAM1102',
        'UPDT': '20230919',
        'UPTI': '1423',
        'UPUS': 'farid.farid'
        }
    ]

# TABLE DETAIL 1101
tbdt101 = [
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '50',
        'EXTD': '0',
        'FEID': 'ROIDM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '1',
        'NMCA': 'Row ID',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'APCDM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'App Code',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'MOCDM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Module Code',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '100',
        'EXTD': '0',
        'FEID': 'MRNAM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Master Name',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'TSTPM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Time Stamp',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'CRUSM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'create user',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPDTM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update Date',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPTIM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update Time',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPUSM1101',
        'FKTO': '0',
        'HEID': 'AAM1101',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update User',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'FEID': 'ROIDM1102',
        'HEID': 'AAM1102',
        'DATY': 'VARCHAR',
        'NMCA': 'Row ID',
        'DEVA': '50',
        'EXTD': '0',
        'ISFK': '0',
        'FKTO': '0',
        'ISPK': '1',
        'STAT': 'active',
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'ITNOM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '1',
        'NMCA': 'Item Code',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '225',
        'EXTD': '0',
        'FEID': 'DESCM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Description',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'IDKSM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'ID Export',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'IDIMM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'ID Import',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'TSTPM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Time Stamp',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'CRUSM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Create User',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPDTM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update Date',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPTIM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update Time',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        },
    {
        'CRDT': '20230919',
        'CRTM': '1422',
        'CRUS': 'farid.farid',
        'DATY': 'VARCHAR',
        'DEVA': '20',
        'EXTD': '0',
        'FEID': 'UPUSM1102',
        'FKTO': '0',
        'HEID': 'AAM1102',
        'ISFK': '0',
        'ISPK': '0',
        'NMCA': 'Update User',
        'STAT': 'active',
        'UPDT': '20230919',
        'UPTI': '1422',
        'UPUS': 'farid.farid'
        }
    
]

# TABLE HEADER 1102
tbha102 = [
    
    ]
# TABLe DETAIL 1102
tbdt102 = [
    ]


# for i in tbha101:
#     cur_sql.execute("""
#                     INSERT INTO AAM1701 (TBIDM1701,CPTBM1701,APNOM1701,APNAM1701,KTAPM1701,QESRM1701,STATM1701,JOINM1701,HISTM1701,EXTTM1701,CRDTM1701,CRTMM1701,CRUSM1701,UPDTM1701,UPTIM1701,UPUSM1701)
#                     VALUES ('{TBID}','{CPTB}','{APNO}','{APNA}','{KTAP}','{QESR}','{STAT}','{JOIN}','{HIST}','{EXTT}','{CRDT}','{CRTM}','{CRUS}','{UPDT}','{UPTI}','{UPUS}')
#                     """.format(
#                     TBID = i['TBID'],
#                     CPTB = i['CPTB'],
#                     APNO = i['APNO'],
#                     APNA = i['APNA'],
#                     KTAP = i['KTAP'],
#                     QESR = i['QESR'],
#                     STAT = i['STAT'],
#                     JOIN = i['JOIN'],
#                     HIST = i['HIST'],
#                     EXTT = i['EXTT'],
#                     CRDT = i['CRDT'],
#                     CRTM = i['CRTM'],
#                     CRUS = i['CRUS'],
#                     UPDT = i['UPDT'],
#                     UPTI = i['UPTI'],
#                     UPUS = i['UPUS']
#                     ))
#     DB_SQL.commit()
#     print("Done !")
    
for o in tbdt101:
    cur_sql.execute("""
            INSERT INTO AAM1801 (FEIDM1801,HEIDM1801,DATYM1801,NMCAM1801,DEVAM1801,EXTDM1801,ISFKM1801,FKTOM1801,ISPKM1801,STATM1801,CRDTM1801,CRTMM1801,CRUSM1801,UPDTM1801,UPTIM1801,UPUSM1801)
            VALUES ('{FEID}','{HEID}','{DATY}','{NMCA}','{DEVA}','{EXTD}','{ISFK}','{FKTO}','{ISPK}','{STAT}','{CRDT}','{CRTM}','{CRUS}','{UPDT}','{UPTI}','{UPUS}')
            """.format(
                FEID = o['FEID'],
                HEID = o['HEID'],
                DATY = o['DATY'],
                NMCA = o['NMCA'],
                DEVA = o['DEVA'],
                EXTD = o['EXTD'],
                ISFK = o['ISFK'],
                FKTO = o['FKTO'],
                ISPK = o['ISPK'],
                STAT = o['STAT'],
                CRDT = o['CRDT'],
                CRTM = o['CRTM'],
                CRUS = o['CRUS'],
                UPDT = o['UPDT'],
                UPTI = o['UPTI'],
                UPUS = o['UPUS']
            ))
    DB_SQL.commit()
    print("Done 2!")