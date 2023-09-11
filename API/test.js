const fs = require('fs')

let dataSB = [{
    key: '0',
    label: 'Documents',
    data: 'Documents Folder',
    icon: 'pi pi-fw pi-inbox',
    children: [
        {
            key: '0-0',
            label: 'Work',
            data: 'Work Folder',
            icon: 'pi pi-fw pi-cog',
            children: [
                { key: '0-0-0', label: 'Expenses.doc', icon: 'pi pi-fw pi-file', data: 'Expenses Document' },
                { key: '0-0-1', label: 'Resume.doc', icon: 'pi pi-fw pi-file', data: 'Resume Document' }
            ]
        },
        {
            key: '0-1',
            label: 'Home',
            data: 'Home Folder',
            icon: 'pi pi-fw pi-home',
            children: [{ key: '0-1-0', label: 'Invoices.txt', icon: 'pi pi-fw pi-file', data: 'Invoices for this month' }]
        }
    ]
},]


let fkey = []

for(let i = 0 ; i < 5 ; i++) {
    let s = `delete from AAMTBDTZ1301 where AAMHAIDZ1302 = 'EXIMT100${i+1}'`
    let ss = `delete from AAMTBHAZ1301 where AAMTBIDZ1302 = 'EXIMT100${i+1}'`
    fkey.push(s)
    fkey.push(ss)
}

let oo1 = "RCST"
let oo2 = "Record Status"
let a = "UPDT"
let a1 = "Update Time"
let b = 'UPTI'
let b1 = "Update time"
let c = 'UPUS'
let c1 = 'Update User'
let d = "CRDT"
let d1 = "Create Date"
let e = "CRTM"
let e1 = "Create Time"
let f = "CRUS"
let f1 = "Create User"

let o = `INSERT INTO AAMTBDTZ1301
        values `


let z0 = `(${oo1}${1+1}01,EXIMT${1+1}01,${oo2},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z1 = `(${a}${1+1}01,EXIMT${1+1}01,${a1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z2 = `(${b}${1+1}01,EXIMT${1+1}01,${b1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z3 = `(${c}${1+1}01,EXIMT${1+1}01,${c1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z4 = `(${d}${1+1}01,EXIMT${1+1}01,${d1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z5 = `(${e}${1+1}01,EXIMT${1+1}01,${e1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`
let z6 = `(${f}${1+1}01,EXIMT${1+1}01,${f1},20,VARCHAR,0,20230831,1447,nugroho.santoso,20230831,1447,nugroho.santoso,0,active)`

let temp = []
for(let y = 0 ; y < 9; y++ ) {
   let z8 =  `  ('${oo1}${y+1}01','EXIMT${y+1}01','${oo2}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${a}${y+1}01','EXIMT${y+1}01','${a1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${b}${y+1}01','EXIMT${y+1}01','${b1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${c}${y+1}01','EXIMT${y+1}01','${c1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${d}${y+1}01','EXIMT${y+1}01','${d1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${e}${y+1}01','EXIMT${y+1}01','${e1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active'),
                ('${f}${y+1}01','EXIMT${y+1}01','${f1}','20','VARCHAR','0','20230831','1447','nugroho.santoso','20230831','1447','nugroho.santoso','0','active')`
    // temp.push(z8)
    let x9 = `${oo1}${y+1}01 VARCHAR(20),
            ${a}${y+1}01 VARCHAR(20),
            ${b}${y+1}01 VARCHAR(20),
            ${c}${y+1}01 VARCHAR(20),
            ${d}${y+1}01 VARCHAR(20),
            ${e}${y+1}01 VARCHAR(20),
            ${f}${y+1}01 VARCHAR(20)
            `
    temp.push(x9)
}

// console.log(fkey)
let res = o + temp.join(",\n")
// console.log(o + temp.join(",\n"));
// console.log(temp.join());
// fs.writeFile("./SQLdoc/addQuery.txt", res, (err) => {
//     if (err)
//       console.log(err);
//     else {
//       console.log("File written successfully\n");
//     //   console.log("The written has the following contents:");
//     //   console.log(fs.readFileSync("books.txt", "utf8"));
//     }
//   });


let temp12 = []

for(let i = 0 ; i < 9;i++) {
    temp12.push(`DROP TABLE EXIMT${i+1}01`)
}
console.log(temp12.join('\n'));