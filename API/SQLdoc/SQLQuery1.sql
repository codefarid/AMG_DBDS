--TestANGAPPS === DB--
use TestAMGAPPS

--Drop Table Untuk Reset jika sudah ada table nya"--
DROP TABLE AAMTBHAZ1301
DROP TABLE AAMTBDTZ1301

-- Table Definition -- 
DROP TABLE AAMTBDEZ1301 
DROP TABLE AAMTCATEZ1301

-- Create Table Definition --
Create Table AAMTBDEZ1301 (
 AAMTBCOZ1302 VARCHAR(20), 
 AAMTDEFZ1302 VARCHAR(60),
 AAMDSTAZ1302 VARCHAR(20),
 AAMDADEZ1302 VARCHAR(20),
 AAMTIDEZ1302 VARCHAR(20),
 AAMCUDEZ1302 VARCHAR(20),
 AAMUDDEZ1302 VARCHAR(20),
 AAMUTDEZ1302 VARCHAR(20),
 AAMUUDEZ1302 VARCHAR(20)
)

select * from AAMTBDEZ1301 
where AAMTDEFZ1302 = 'Approval Request Amount'

DELETE FROM AAMTBDEZ1301
WHERE AAMTBCOZ1302 = 'OPIR'

ALTER TABLE AAMTBDEZ1301
ALTER COLUMN AAMTBCOZ1302 VARCHAR(20) NOT NULL;

ALTER TABLE AAMTBDEZ1301
ADD CONSTRAINT PK_AAMTBDEZ1301 PRIMARY KEY (AAMTBCOZ1302);

ALTER TABLE AAMTBDEZ1301
ADD CONSTRAINT UQ_AAMTDEFZ1302 UNIQUE (AAMTDEFZ1302);

Select AAMTDEFZ1302 as caption from AAMTBDEZ1301 where AAMTDEFZ1302 = 'AMG Approval'

-- Create Table Categories -- 
CREATE TABLE AAMTCATEZ1301 (
  AAMCAVAZ1302 VARCHAR(20), 
  AAMCKEYZ1302 VARCHAR(90),
  AAMCSTAZ1302 VARCHAR(20),
  AAMDACAZ1302 VARCHAR(20),
  AAMTACAZ1302 VARCHAR(20),
  AAMUSCAZ1302 VARCHAR(20),
  AAMUDACZ1302 VARCHAR(20),
  AAMUTACZ1302 VARCHAR(20),
  AAMUUSCZ1302 VARCHAR(20)
  )

--Create Table_Header--
CREATE TABLE AAMTBHAZ1301  (
  AAMTBIDZ1302 VARCHAR(20)NOT NULL PRIMARY KEY,
  AAMCPTBZ1302 VARCHAR(60),
  AAMALIDZ1302 VARCHAR(20),
  AAMALNMZ1302 VARCHAR(20),        
  AAMKTAPZ1302 VARCHAR(20),
  AAMQESRZ1302 TEXT,
  AAMJOINZ1302 VARCHAR(60),
  AAMTHSTZ1302 VARCHAR(20),
  AAMCEATZ1302 VARCHAR(8),
  AAMCETMZ1302 VARCHAR(8),
  AAMCEUEZ1302 VARCHAR(30),
  AAMUDATZ1302 VARCHAR(8),
  AAMUDTMZ1302 VARCHAR(8),
  AAMUDUEZ1302 VARCHAR(30)
  )
  alter table AAMTBHAZ1301 add AAMTHISZ1301 TEXT
  alter table AAMTBHAZ1301 add AAMEXTTZ1301 VARCHAR(20)
  --Create Table_Detail--
  -- jangan lupa abis drop buat id jd pk juga --
CREATE TABLE AAMTBDTZ1301 (
  AAMFEIDZ1302 VARCHAR(20) NOT NULL,
  AAMHAIDZ1302 VARCHAR(20) NOT NULL,
  AAMNMZ1302 VARCHAR(60),
  AAMVLZ1302 VARCHAR(20),
  AAMDTZ1302 VARCHAR(20),
  AAMPKZ1302 VARCHAR(10),
  AAMCEATZ1302 VARCHAR(8),
  AAMCETMZ1302 VARCHAR(8),
  AAMCEUEZ1302 VARCHAR(30),
  AAMUDATZ1302 VARCHAR(8),
  AAMUDTMZ1302 VARCHAR(8),
  AAMUDUEZ1302 VARCHAR(30),
  CONSTRAINT PK_AAMTBDTZ1301 PRIMARY KEY (AAMHAIDZ1302, AAMFEIDZ1302)
);
alter table AAMTBDTZ1301 add AAMEXTDZ1301 VARCHAR(20)
alter table AAMTBDTZ1301 add AAMSTTDZ1301 VARCHAR(20)
alter table AAMTBDTZ1301 add AAMISFKZ1301 VARCHAR(20)
alter table AAMTBDTZ1301 add AAMFKTOZ1301 VARCHAR(20)

--Read Table Header--
SELECT * FROM AAMTBHAZ1301
Select 
  AAMTBIDZ1302 as table_id ,
  AAMCPTBZ1302 as caption_table,
  AAMALIDZ1302 as aplication_id,
  AAMALNMZ1302 as aplication_name,        
  AAMKTAPZ1302 as kategori_app,
  AAMQESRZ1302 as query_string ,
  AAMTHSTZ1302 as stat,
  AAMJOINZ1302 as joinTo,
  AAMTHISZ1301 as history,
  AAMEXTTZ1301 as existing,
  AAMCEATZ1302 as "created_At" ,
  AAMCETMZ1302 as "created_Time" ,
  AAMCEUEZ1302 as "created_user"  ,
  AAMUDATZ1302 as "updated_at" ,
  AAMUDTMZ1302 as "updated_time" ,
  AAMUDUEZ1302 as "updated_user" 
  from AAMTBHAZ1301 where AAMTHSTZ1302 = 'active' 
  order by AAMCEATZ1302 DESC

  Select TOP 1 AAMCPTBZ1302 as caption from AAMTBHAZ1301 order by AAMTBIDZ1302 DESC
  Select TOP 1 AAMCPTBZ1302 as caption from AAMTBHAZ1301 order by AAMTBIDZ1302 DESC
  Select TOP 1 AAMCAVAZ1302 as value from AAMTCATEZ1301 order by AAMCAVAZ1302 DESC

Select TOP 1
AAMTBIDZ1302 as table_id ,  
AAMCPTBZ1302 as caption_table,
AAMALIDZ1302 as aplication_id,
AAMALNMZ1302 as aplication_name,
AAMKTAPZ1302 as kategori_app
From AAMTBHAZ1301
Where AAMALNMZ1302 = 'Home Apps' and AAMKTAPZ1302 = '1'
ORDER by AAMTBIDZ1302 DESC

select * from AAMTBHAZ1301

-- Read Table Detail--
SELECT * FROM AAMTBDTZ1301
Select 
  AAMFEIDZ1302 as field_id ,
  AAMHAIDZ1302 as header_id ,
  AAMNMZ1302 as name_caption,
  AAMVLZ1302 as default_value,
  AAMDTZ1302 as data_type,
  AAMPKZ1302 as is_pk,
  AAMEXTDZ1301 as isExistingField,
  AAMSTTDZ1301 as "Status Table",
  AAMCEATZ1302 as "created_At" ,
  AAMCETMZ1302 as "created_Time" ,
  AAMCEUEZ1302 as "created_user"  ,
  AAMUDATZ1302 as "updated_at" ,
  AAMUDTMZ1302 as "updated_time" ,
  AAMUDUEZ1302 as "updated_user" 
  from AAMTBDTZ1301 where AAMHAIDZ1302 = 'DOMSM201' AND AAMSTTDZ1301 = 'active' ORDER BY AAMHAIDZ1302 DESC


  UPDATE AAMTBDTZ1301 
  SET AAMSTTDZ1301 = 'active'
  where AAMSTTDZ1301 = 'inactive'

  select * from AAMTBDTZ1301 

  select * from AAMTBHAZ1301



SELECT TOP 1
AAMTBIDZ1302 as table_id ,
AAMCPTBZ1302 as caption_table,
AAMALIDZ1302 as aplication_id,
AAMALNMZ1302 as aplication_name, 
AAMKTAPZ1302 as kategori_app, 
AAMJOINZ1302 as joined
from AAMTBHAZ1301
where (AAMALNMZ1302 = 'Home Apps' and AAMKTAPZ1302 = '1' and AAMJOINZ1302 = 'AAM202')
order by AAMTBIDZ1302 desc

SELECT 
AAMTBIDZ1302 as table_id ,
AAMCPTBZ1302 as caption_table,
AAMALIDZ1302 as aplication_id,
AAMALNMZ1302 as aplication_name, 
AAMKTAPZ1302 as kategori_app, 
AAMJOINZ1302 as joined
from AAMTBHAZ1301
where (AAMALNMZ1302 = 'Home Apps' and AAMKTAPZ1302 = '1')

SELECT top 1 AAMCPTBZ1302 FROM AAMTBHAZ1301
WHERE AAMCPTBZ1302 like '%Aplication Transaction%'

DELETE FROM AAMTCATEZ1301
WHERE AAMCKEYZ1302 = 'Report'
select * from AAMTCATEZ1301

-- Read Sugestions--
select AAMTBCOZ1302 as code, AAMTDEFZ1302 as label, AAMCUDEZ1302 as 'user', AAMDSTAZ1302 as 'status' from AAMTBDEZ1301 where 
select * from AAMTBDEZ1301
select
AAMTBCOZ1302 as 'code',
AAMTDEFZ1302 as 'value',
AAMDSTAZ1302 as 'status'
from AAMTBDEZ1301 
where AAMTBCOZ1302 = 'NOPN'

 
Select TOP 1 AAMTBCOZ1302 as 'code',AAMTDEFZ1302 as 'text' from AAMTBDEZ1301 order by AAMUDDEZ1302 DESC

-- READ CATEGORIES-- 
select AAMCAVAZ1302 as code ,
 AAMCKEYZ1302 as label,
  AAMDACAZ1302 as 'created', 
  AAMUSCAZ1302 as 'user',
   AAMCSTAZ1302 as status 
   from AAMTCATEZ1301
select * from AAMTCATEZ1301



-- Get All Apps Name for dropdown

SELECT AMAPNA101 as 'App_Name' from AAM101
  WHERE AMAPCA101 <> 'Trial' AND AMAPSH101 <> 'NULL'

-- Get First Code for id
Select AMAPSH101 AS 'first_string', AMAPNA101 as 'app_name', AMAPCA101 as 'app_id' from AAM101
  WHERE AMAPCA101 <> 'Trial' AND AMAPNA101 = 'Document Management'

SELECT AAMTBIDZ1302 as 'id' from AAMTBHAZ1301 WHERE AAMKTAPZ1302 = 2

SELECT AAMTBIDZ1302 as table_id , AAMCPTBZ1302 as caption_table
  from AAMTBHAZ1301 

SELECT AAMQESRZ1302 AS query_exist
  FROM AAMTBHAZ1301 
  WHERE AAMTBIDZ1302 = 'DOMST201'

SELECT AAMALIDZ1302 as 'aplication_id', AAMALNMZ1302 as 'aplication_name' from AAMTBHAZ1301 where AAMALNMZ1302 = 'Document Management'

-- Get One app by app_code --
SELECT AMAPCA101 as 'App_Code', AMAPNA101 as 'App_Name' from AAM101
 WHERE AMAPCA101 = '2022-07-APPCT-0003' AND AMAPNA101 = 'Document Management'
 WHERE AAMHAIDZ1302 = 'AAM201'


 use testAMGAPPS

 select * from aam501
 where AMUSNO501 like 'santoso'
 where AMUSNO501 like '%nugroho.santoso%'
 
 SELECT
 AAMTBCOZ1302 as 'value',
 AAMTDEFZ1302 as 'key',
 AAMDSTAZ1302 as 'status' 
 FROM AAMTBDEZ1301 where AAMTDEFZ1302 like '%Export%'

  SELECT
 AAMTBCOZ1302 as 'value',
 AAMTDEFZ1302 as 'key',
 AAMDSTAZ1302 as 'status' 
 FROM AAMTBDEZ1301 where AAMTBCOZ1302 like '%NO%'

update AAMTBDEZ1301 set AAMTBCOZ1302 = 'CDEX' where AAMTBCOZ1302 = 'CDES'
update AAMTBDEZ1301 set AAMTDEFZ1302 = 'Negara Tujuan Ekspor' where AAMTDEFZ1302 = 'Negara Tujuan'

SELECT 
AAMTBHAZ1301.AAMTBIDZ1302 AS data1,
AAMTBHAZ1301.AAMCPTBZ1302 AS label1,
AAMTBDTZ1301.AAMFEIDZ1302 AS data2,
AAMTBDTZ1301.AAMNMZ1302 AS label2
FROM AAMTBHAZ1301
left join
AAMTBDTZ1301 ON AAMTBHAZ1301.AAMTBIDZ1302 = AAMTBDTZ1301.AAMHAIDZ1302
where AAMTHSTZ1302 = 'active' and AAMTBDTZ1301.AAMSTTDZ1301 = 'active'

select * from AAMTBHAZ1301


SELECT * FROM AAMTBDTZ1301
where AAMSTTDZ1301 = 'active'

SELECT    
AAMTBHAZ1301.AAMTBIDZ1302 AS table_id,
AAMTBHAZ1301.AAMCPTBZ1302 AS caption_table,
AAMTBDTZ1301.AAMFEIDZ1302 AS field_id,
AAMTBDTZ1301.AAMHAIDZ1302 AS header_id,
AAMTBDTZ1301.AAMNMZ1302 AS name_caption
FROM
AAMTBHAZ1301
INNER JOIN 
AAMTBDTZ1301 ON AAMTBHAZ1301.AAMTBIDZ1302 = AAMTBDTZ1301.AAMHAIDZ1302
where AAMTHSTZ1302 = active
use TestAMGAPPS


select * from AAMTBHAZ1301 
select * from AAMTBDTZ1301

use TestAMGAPPS

delete from AAMTBHAZ1301 where AAMTBIDZ1302 = 'EXIMT1003'
delete from AAMTBDTZ1301 where AAMHAIDZ1302 = 'EXIMT1003'
update AAMTBDEZ1301 set AAMTDEFZ1302 = 'Satuan Tipe' where AAMTDEFZ1302 = 'Satyan Type'

Select TOP 1
AAMTBIDZ1302 as table_id ,
AAMCPTBZ1302 as caption_table,
AAMALIDZ1302 as aplication_id,
AAMALNMZ1302 as aplication_name,
AAMKTAPZ1302 as kategori_app
From AAMTBHAZ1301
Where AAMALNMZ1302 = 'EXIM SYSTEM' and AAMKTAPZ1302 = '2'
ORDER by AAMTBIDZ1302 DESC    

Select
AAMTBIDZ1302 as table_id 
From AAMTBHAZ1301
Where AAMALNMZ1302 = 'EXIM SYSTEM' and AAMKTAPZ1302 = '2'
order by len(AAMTBIDZ1302) asc



use TestAMGAPPS

CREATE TABLE AAM1101 (
ROID1101 varchar(50) not null primary key ,
APCD1101 varchar(20),
MOCD1101 varchar(20),
MRNA1101 varchar(20),
TSTP1101 varchar(20),
CRUS1101 varchar(20),
UPDT1101 varchar(20),
UPTI1101 varchar(20),
UPUS1101 varchar(20)
)

SELECT * FROM AAM1101
select 
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

create table AAM1102 (
ROID1102 varchar(50) Primary key,
ITNO1102 varchar(20),
DESC1102 varchar(20),
IDKS1102 varchar(20),
IDIM1102 varchar(20),
IDMC1102 varchar(20),
TSTP1102 varchar(20),
CRUS1102 varchar(20),
UPDT1102 varchar(20),
UPTI1102 varchar(20),
UPUS1102 varchar(20)
)



ALTER TABLE EXIMT301 DROP CONSTRAINT FK_IDETT301
DROP TABLE EXIMT301

select * from EXIMT301

use TestAMGAPPS
use TestAMGAPPS
select AAMTBIDZ1302 as 'TABLE_NAME' from AAMTBHAZ1301
where AAMTHSTZ1302 = 'active'

SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'AAMTCATEZ1301'
EXEC sp_columns 'AAMTBDEZ1301'

select * from AAM1101
use AMGAPPS