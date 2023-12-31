-- Create Query for PR Form --
CREATE TABLE PRMTT101 (
IDNOT101 VARCHAR(225) not null Primary Key,
DCIDT101 VARCHAR(225),
ITNAT101 VARCHAR(225),
SPSFT101 VARCHAR(1000),
JNPTT101 VARCHAR(225),
ESTDT101 VARCHAR(225),
ESTPT101 INT,
QTYPT101 INT,
UNITT101 VARCHAR(225),
REMAT101 VARCHAR(225),
USNOT101 VARCHAR(225),
PSTDT101 VARCHAR(225),
KTPRT101 VARCHAR(225),
STATT101 VARCHAR(20),
STPRT101 VARCHAR(225),
NBSGT101 VARCHAR(225),
CRDTT101 VARCHAR(225),
CRTMT101 VARCHAR(225),
CRUST101 VARCHAR(225),
UPDTT101 VARCHAR(225),
UPTIT101 VARCHAR(225),
UPUST101 VARCHAR(225)
);
ALTER TABLE PRMTT101
ADD CCNOT101 VARCHAR(25);

alter table PRMTT101
ADD NSGNT101 varchar(225);

select * from AAMPRFM1501;
select count(*) from AAMPRFM1501;
-- Select Query for PR Form --
SELECT
IDNOT101 as 'column_id',
DCIDT101 as 'document_id',
ITNAT101 as 'nama_barang',
SPSFT101 as 'spesifikasi',
JNPTT101 as 'jenis_parts',
ESTDT101 as 'est_pemakaian',
ESTPT101 as 'est_price',
QTYPT101 as 'jumlah_angka',
UNITT101 as 'satuan',
REMAT101 as 'remarks',
USNOT101 as 'user',
PSTDT101 as 'posting_date',
KTPRT101 as 'keterangan',
STATT101 as 'status',
STPRT101 as 'status_form',
NBSGT101 as 'nama_barang_storeGoods',
CCNOT101 as 'cost_center',
CRDTT101 as 'Create Date',
CRTMT101 as 'Create Time',
CRUST101 as 'Create User',
UPDTT101 as 'Update Date',
UPTIT101 as 'Update Time',
UPUST101 as 'Update User'
FROM PRMTT101;
