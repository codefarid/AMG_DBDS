const fs = require("fs");

// fs.readFile('./SQLdoc/code.txt', 'utf-8', (err, data) => {
//     if(err) return err
//     let data1 = data.trim().split('\r\n')
//     let query = `INSERT INTO AAMTBDEZ1301 (AAMTBCOZ1302) `
//     query += `VALUES \n`
//     // tambahkan kondisi pada map jika i tidak lebih dari 999
//     let val = data1.slice(0,1000).map((el) => `\t('${el}')`).join(',\n')

//     query += val
//     fs.writeFile('./SQLdoc/query1.txt', query, (err) => {
//         if(err) return err
//         console.log("query insert into code success!")
//     })
// })

// fs.readFile('./SQLdoc/definition.txt', 'utf-8', (err, data) => {
//     if(err) return err
//     let data1 = data.trim().split('\r\n')
//     let query = `INSERT INTO AAMTBDEZ1301 (AAMTDEFZ1302) `
//     query += `VALUES \n`
//     let val = data1.slice(0,1000).map((el) => `\t('${el}')`).join(',\n')
//     query += val
//     fs.writeFile('./SQLdoc/query2.txt', query, (err) => {
//         if(err) return err
//         console.log("query inseret into definition success!")
//     })
// })

// fs.readFile('./SQLdoc/code.txt', 'utf-8', (err, data) => {
//     if(err) return err
//     let data1 = data.trim().split('\r\n')
//     let query = `INSERT INTO AAMTBDEZ1301 (AAMTBCOZ1302) `
//     query += `VALUES \n`
//     // tambahkan kondisi i lebih dari 1000
//     let val = data1.map((el,i) => i >= 1000 ? `\t('${el}')` : delete el).join(',\n')

//     query += val
//     fs.writeFile('./SQLdoc/query1k.txt', query, (err) => {
//         if(err) return err
//         console.log("query 1k above insert into code success!")
//     })
// })

// fs.readFile('./SQLdoc/definition.txt', 'utf-8', (err, data) => {
//     if(err) return err
//     let data1 = data.trim().split('\r\n')
//     let query = `INSERT INTO AAMTBDEZ1301 (AAMTBCOZ1302) `
//     query += `VALUES \n`
//     // tambahkan kondisi i lebih dari 1000
//     let val = data1.map((el,i) => i >= 1000 ? `\t('${el}')` : delete el).join(',\n')

//     query += val
//     fs.writeFile('./SQLdoc/query2k.txt', query, (err) => {
//         if(err) return err
//         console.log("query 1k above insert into definition success!")
//     })
// })
// const data1 = fs.readFileSync('./SQLdoc/code.txt', { encoding: 'utf8', flag: 'r' }).trim().split('\r\n')
// const data2 = fs.readFileSync('./SQLdoc/definition.txt', { encoding: 'utf8', flag: 'r' }).trim().split('\r\n')

// if(data1.length === data2.length){
//     let result1 = []
//     let result2 = []
//     let query1 = `INSERT INTO AAMTBDEZ1301 ( AAMTBCOZ1302 , AAMTDEFZ1302 , AAMDSTAZ1302 , AAMDADEZ1302, AAMTIDEZ1302, AAMCUDEZ1302, AAMUDDEZ1302, AAMUTDEZ1302, AAMUUDEZ1302) VALUES \n`
//     let query2 = `INSERT INTO AAMTBDEZ1301 ( AAMTBCOZ1302 , AAMTDEFZ1302 , AAMDSTAZ1302 , AAMDADEZ1302, AAMTIDEZ1302, AAMCUDEZ1302, AAMUDDEZ1302, AAMUTDEZ1302, AAMUUDEZ1302) VALUES \n`
//     let path = ''

//     var today  = new Date();
//     var getDate = today.toLocaleDateString("id-ID").split("/").join("")
//     var getTime = today.toLocaleTimeString().split(":").splice(0,2).join("")
//     var getStatus = 'active'
//     var user = "santoso"

//     result1 = data1.slice(0,1000).map((code , index) => {
//         return {
//             code : code ,
//             definition : data2[index],
//             status: getStatus,
//             date : getDate,
//             time : getTime,
//             user: user
//         }
//     })
//     query1 += result1.map(el => `\t('${el.code}', '${el.definition}', '${el.status}','${el.date}', '${el.time}', '${el.user}', '${el.date}', '${el.time}', '${el.user}')`).join(",\n")
//     path = "SQLdoc/query1.sql"

//     fs.writeFile(path, query1, (err) => {
//                     if(err) return err
//                     console.log("query 1 write file query1.sql!")
//         })

//     if(data1.length > 1000) {
//         result2 = data1.slice(1000).map((code , index) => {
//             return {
//                 code : code ,
//                 definition : data2[index + 1000],
//                 status: getStatus,
//                 date : getDate,
//                 time : getTime,
//                 user: user
//             }
//         })
//         query2 += result2.map(el => `\t('${el.code}', '${el.definition}', '${el.status}','${el.date}', '${el.time}', '${el.user}', '${el.date}', '${el.time}', '${el.user}')`).join(",\n")
//         path = "SQLdoc/queryMoreThan1k.sql"
//         fs.writeFile(path, query2, (err) => {
//             if(err) return err
//             console.log("query 1k above write success!")
//             })
//     }

// }
// convert to python and simplified

// # -- Merubah nama kolom
// # ALTER TABLE nama_tabel RENAME COLUMN nama_kolom_lama TO nama_kolom_baru;

// # -- Merubah tipe data kolom
// # ALTER TABLE nama_tabel ALTER COLUMN nama_kolom TYPE tipe_data;

// # -- Set kolom sebagai primary key
// # ALTER TABLE nama_tabel ADD CONSTRAINT nama_konstrain PRIMARY KEY (nama_kolom);

// var today  = new Date();
// var getDate = today.toLocaleDateString("id-ID").split("/").join("")
// var getTime = today.toLocaleTimeString().split(":").splice(0,2).join("")
// var user = "santoso"

// let query = `INSERT INTO AAMTCATEZ1301 (AAMCAVAZ1302, AAMCKEYZ1302, AAMDACAZ1302, AAMTACAZ1302, AAMUSCAZ1302, AAMUDACZ1302, AAMUTACZ1302, AAMUUSCZ1302) VALUES\n`
// let val1 = `\t('1','Master', '${getDate}', '${getTime}', '${user}', '${getDate}', '${getTime}', '${user}'),\n`
// let val2 = `\t('2','Transaction', '${getDate}', '${getTime}', '${user}', '${getDate}', '${getTime}', '${user}')`
// console.log(query,val1,val2)

// bagaimana membuat ini
// let dataTable = [
//     {
//         "caption": "Level",
//         "id": "DOMSM101",
//         "query": "Create Table DOMSM201 (\n\tVANAM201 VARCHAR(123),\n\tVANOM201 VARCHAR(123) NOT NULL PRIMARY KEY,\n\tVALUM201 VARCHAR(1233)\n)",
//         "status": "active"
//     },
//     {
//         "caption": "Join Level",
//         "id": "DOMSM102",
//         "query": "Create Table DOMSM102 (\n\tDNA7M102 VARCHAR(12333),\n\tVANOM102 VARCHAR(123) NOT NULL PRIMARY KEY,\n\tCOFLM102 VARCHAR(1233)\n)",
//         "status": "active"
//     },
//     {
//         "caption": "Test Join Existing",
//         "id": "JOTEM102",
//         "query": "Create Table JOTEM102 (\n\tDENOM102 VARCHAR(60) NOT NULL PRIMARY KEY,\n\tDENSM102 VARCHAR(1233)\n)",
//         "status": "active"
//     },
//     {
//         "caption": "Test Existing",
//         "id": "TESTM101",
//         "query": "Create Table DOMSM201 (\n\tTEF1M201 VARCHAR(123) NOT NULL PRIMARY KEY,\n\tTEF2M201 VARCHAR(123),\n\tVANOM201 VARCHAR(12333),\n\tAPDTM201 BINARY(12333)\n)",
//         "status": "active"
//     }
// ]

// let fieldsPerTable = [
//     {
//         "headerId": "DOMSM101",
//         "totalField": 3
//     },
//     {
//         "headerId": "DOMSM102",
//         "totalField": 3
//     },
//     {
//         "headerId": "JOTEM102",
//         "totalField": 2
//     },
//     {
//         "headerId": "TESTM101",
//         "totalField": 4
//     }
// ]

// let mergedArray = dataTable.map(data => {
//     let fields = fieldsPerTable.find(field => field.headerId === data.id);
//     return { ...data, ...fields };
//   });

// console.log(mergedArray);

// const data = {
//                 tableName: "Folder",
//                 isMaster: {
//                     key: "Master",
//                     status: "active",
//                     value: "1",
//                 },
//                 extName: null,
//                 appName: {
//                     text: "Document Management",
//                     value: "DOMS",
//                 },
//                 joinTo: null,
//                 status: null,
//                 field: [
//                     {
//                     extFname: "",
//                     fieldName: {
//                         key: "Variable Code",
//                         status: "active",
//                         value: "VANO",
//                     },
//                     datTypeField: "varchar",
//                     maxlenField: 669,
//                     isPk: true,
//                     },
//                     {
//                     extFname: "",
//                     fieldName: {
//                         key: "Variable Name",
//                         status: "active",
//                         value: "VANA",
//                     },
//                     datTypeField: "varchar",
//                     maxlenField: 60,
//                     isPk: false,
//                     },
// {
//     extFname: "",
//     fieldName: {
//         key: "Variable CodeT",
//         status: "active",
//         value: "VANT",
//     },
//     datTypeField: "varchar",
//     maxlenField: 669,
//     isPk: true,
//     },
//     {
//     extFname: "",
//     fieldName: {
//         key: "Variable NameX",
//         status: "active",
//         value: "VANX",
//     },
//     datTypeField: "varchar",
//     maxlenField: 60,
//     isPk: false,
//     },
//     {
//         extFname: "",
//         fieldName: {
//             key: "Variable CodeS",
//             status: "active",
//             value: "VANS",
//         },
//         datTypeField: "varchar",
//         maxlenField: 669,
//         isPk: true,
//         },
//         {
//         extFname: "",
//         fieldName: {
//             key: "Variable Eame",
//             status: "active",
//             value: "VANR",
//         },
//         datTypeField: "varchar",
//         maxlenField: 60,
//         isPk: false,
//         },
// ],
// };

// function generateIdHeader(obj) {
//     let a = obj.appName.value
//     let b = obj.isMaster.key[0]
//     let c = 101
//     return a + b + c.toString()
// }

// function generateIdTDetail(input, headerId) {
//     let a = headerId.slice(4)
//     return input + a
// }

// function postQuery(obj) {
//     let result = []
//     let headerId = generateIdHeader(obj)
//     let query1 = `CREATE TABLE ${headerId} (`

//     let fieldIds = obj.field.filter((el) => el.isPk == true).map((el) => generateIdTDetail(el.fieldName.value, headerId))
//     let counterPk = fieldIds.length
//     let last = `CONSTRAINT PK_${headerId} PRIMARY KEY (${fieldIds.join(', ')})`

//     let fields = obj.field.map((el) => {
//         return `${generateIdTDetail(el.fieldName.value, headerId)} ${el.datTypeField}(${el.maxlenField})`
//     })

//     if(counterPk > 1) {
//         result = fields
//         result.unshift(query1)
//         result.push(last)
//         result.push(')')
//         return result.join("?")
//     } else {
//         let fieldss = obj.field.map((el) => {
//             let isPKs = el.isPk ? 'NOT NULL PRIMARY KEY' : '';
//             return `${generateIdTDetail(el.fieldName.value, headerId)} ${el.datTypeField}(${el.maxlenField}) ${isPKs}`
//         })
//         result = fieldss
//         result.unshift(query1)
//         result.push(')')
//         return result.join("?")
//     }
// }

// console.log(postQuery(data));

// const s = "DOMSM404"
// console.log(s.slice(0,4))
// let abc = {
//     "tableName": "Master Application",
//     "extTableName": "",
//     "isMaster": {
//         "key": "Master",
//         "status": "active",
//         "value": "1"
//     },
//     "extName": "",
//     "appName": {
//         "text": "Home Apps",
//         "value": "AA"
//     },
//     "status": "active",
//     "field": [
//         {
//             "extFname": {
//                 "key": "Application Create"
//             },
//             "fieldName": "AACRM203",
//             "maxlenField": 1213,
//             "datTypeField": "varchar",
//             "isPk": false
//         },
//         {
//             "extFname": {
//                 "key": "Application Definition"
//             },
//             "fieldName": "AADEM101",
//             "maxlenField": 123,
//             "datTypeField": "varchar",
//             "isPk": false
//         },
//         {
//             "extFname": {
//                 "key": "Aplication Id"
//             },
//             "fieldName": "AAMID101",
//             "maxlenField": 123,
//             "datTypeField": "varchar",
//             "isPk": true
//         },
//         {
//             "extFname": {
//                 "key": "Application Name",
//                 "status": "active",
//                 "value": "APNA"
//             },
//             "fieldName": "AANAM202",
//             "maxlenField": 213,
//             "datTypeField": "varchar",
//             "isPk": true
//         },
//         {
//             "extFname": "Aplication Code",
//             "fieldName": "AACOM202",
//             "datTypeField": "varchar",
//             "maxlenField": 123,
//             "isPk": false
//         },
//         {
//             "extFname": {
//                 "key": "Application Default URL",
//                 "status": "active",
//                 "value": "AURL"
//             },
//             "fieldName": "AAPRM202",
//             "datTypeField": "varchar",
//             "maxlenField": 123,
//             "isPk": false
//         }
//     ]
// }

// let x = "{'value': 'AAQTR101'} varchar(123)"
// let y = "D2QTR101 char(12)"

// function checkParse(val) {
//     if(val[0] == "{"){
//         let a = val.slice(11,19)
//         let b = val.slice(21)
//         return a + b
//     } else {
//         return val
//     }
// }

// console.log(checkParse(x))

// let b = "{'value': 'AAQTR101'} varchar(123)"
// console.log(b.length)

// let akmj = [{'ids': 'AAM101'}, {'ids': 'AAM102'}, {'ids': 'AAM103'}, {'ids': 'AAM201'}];

// let bbb = akmj.map((el) => `DELETE FROM AAMTBDTZ1301
// WHERE AAMHAIDZ1302 = '${el.ids}'
//   DELETE FROM AAMTBHAZ1301
// WHERE AAMTBIDZ1302 = '${el.ids}' `).join('\n')
// console.log(bbb)


let objay = {
  "tableName": "Aplication Existing",
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
  "isExisted": "1",
  "field": [
      {
          "fieldNameEdit": {
              "key": "AABMM201"
          },
          "extFname": {
              "key": "Aplication Budget"
          },
          "fieldName": {
              "value": "AABMM201"
          },
          "maxlenField": 123,
          "datTypeField": "varchar",
          "isPk": false,
          "statTD": "inactive"
      },
      {
          "fieldNameEdit": {
              "key": "AACOM201"
          },
          "extFname": {
              "key": "Aplication Code"
          },
          "fieldName": {
              "value": "AACOM201"
          },
          "maxlenField": 50,
          "datTypeField": "varchar",
          "isPk": false,
          "statTD": "active"
      },
      {
          "fieldNameEdit": {
              "key": "AAMID201"
          },
          "extFname": {
              "key": "Aplication ID"
          },
          "fieldName": {
              "value": "AAMID201"
          },
          "maxlenField": 60,
          "datTypeField": "varchar",
          "isPk": true,
          "statTD": "active"
      },
      {
          "fieldNameEdit": {
              "key": "AAVEM201"
          },
          "extFname": {
              "key": "Aplication Vendor"
          },
          "fieldName": {
              "value": "AAVEM201"
          },
          "maxlenField": 123,
          "datTypeField": "varchar",
          "isPk": false,
          "statTD": "inactive"
      }
  ]
}


let wy = objay.field.filter((data) => data.statTD == 'active')
let temp = {
  "tableName": objay.tableName,
  "extTableName": objay.extTableName,
  "isMaster":objay.isMaster,
  "extName": objay.extName,
  "appName": objay.appName,
  "joinTo": objay.joinTo,
  "status": objay.status,
  "isExisted": objay.isExisted,
  "field": wy
}

console.log(temp)