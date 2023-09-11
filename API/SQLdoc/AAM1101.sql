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

select 
    ROID1101 as 'Row ID',
    APCD1101 as 'App Code',
    MOCD1101 as 'Module Code',
    MRNA1101 as 'Master Name',
    TSTP1101 as 'Time Stamp',
    CRUS1101 as 'create user',
    UPDT1101 as 'Update Date',
    UPTI1101 as 'Update Time',
    UPUS1101 as 'Update User'
from AAM1101

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

select 
    ROID1102 as 'Row ID',
    ITNO1102 as 'Item Code',
    DESC1102 as 'Description',
    IDKS1102 as 'ID Export',
    IDIM1102 as 'ID Import',
    IDMC1102 as 'IDOMA Code',
    TSTP1102 as 'Time Stamp',
    CRUS1102 as 'Create User',
    UPDT1102 as 'Update Date',
    UPTI1102 as 'Update Time',
    UPUS1102 as 'Update User'
from AAM1102