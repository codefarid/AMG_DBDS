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

EXEC sp_rename 'AAM1101.ROID1101' , 'ROIDM1101'
EXEC sp_rename 'AAM1101.APCD1101' , 'APCDM1101'
EXEC sp_rename 'AAM1101.MOCD1101' , 'MOCDM1101'
EXEC sp_rename 'AAM1101.MRNA1101' , 'MRNAM1101'
EXEC sp_rename 'AAM1101.TSTP1101' , 'TSTPM1101'
EXEC sp_rename 'AAM1101.CRUS1101' , 'CRUSM1101'
EXEC sp_rename 'AAM1101.UPDT1101' , 'UPDTM1101'
EXEC sp_rename 'AAM1101.UPTI1101' , 'UPTIM1101'
EXEC sp_rename 'AAM1101.UPUS1101' , 'UPUSM1101'

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

EXEC sp_rename 'AAM1102.ROID1102' , 'ROIDM1102'
EXEC sp_rename 'AAM1102.ITNO1102' , 'ITNOM1102'
EXEC sp_rename 'AAM1102.DESC1102' , 'DESCM1102'
EXEC sp_rename 'AAM1102.IDKS1102' , 'IDKSM1102'
EXEC sp_rename 'AAM1102.IDIM1102' , 'IDIMM1102'
EXEC sp_rename 'AAM1102.IDMC1102' , 'IDMCM1102'
EXEC sp_rename 'AAM1102.TSTP1102' , 'TSTPM1102'
EXEC sp_rename 'AAM1102.CRUS1102' , 'CRUSM1102'
EXEC sp_rename 'AAM1102.UPDT1102' , 'UPDTM1102'
EXEC sp_rename 'AAM1102.UPTI1102' , 'UPTIM1102'
EXEC sp_rename 'AAM1102.UPUS1102' , 'UPUSM1102'

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