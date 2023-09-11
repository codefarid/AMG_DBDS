import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { FormBuilder, FormGroup, Validators, FormArray, FormControl, Form } from '@angular/forms';
import {
    LazyLoadEvent,
    MessageService,
    ConfirmationService,
    ConfirmEventType
} from 'primeng/api';
import { MasterService } from 'src/app/service/master.service';
import { DropdownLevel } from 'src/app/_model/dropdown-value.model';
import { Dictionary } from 'src/app/_model/dictionary.model';

@Component({
    selector: 'app-dbds',
    templateUrl: './dbds.component.html',
    styleUrls: ['./dbds.component.scss'],
})
export class DBDSComponent implements OnInit {
    isEdit = false;
    isExistingTable = false
    editExistingTable = false
    editableDatas: any[] = []
    modalTitle = '';
    displayForm = false;
    isLoadingButton = false;
    loading = false;
    previewQuery = false;
    showIsjoin = false;
    displayQuery = '';
    displayOneQuery = false;
    downloadQuery = false;
    editMasterTable = false
    fieldStatus = false;
    blockedFields : boolean[] = [];
    displayQueryAfter: string[] = [];
    getId = '';
    totalRecord = 0 ;
    maxLenValidator = 0;
    totalStoredQuery = 0
    loadSugestionInit = false

    selectedCategories: any;
    selectedAplications: any;
    selectedSugestions: any;
    createdFileName:any;

    displayQuerySelect: any[] = []
    columnNameList: any [] = []
    whereOperandList: any[] = []
    orOperanList: any[] = []
    addNewWhere = false
    addNewOr = false
    selectAorDESC: any
    loadSelectQuery = false
    dataQuerySelect:any
    disableWhere = false
    disableOr = false
    disableBetween = false
    disableOrderBy = false
    disableSkipRows = false
    disableFetchOnly = false
    readyToDownloads = false
    fkey!: any[];
    editTableDetail: any[] = [];
    fieldIdRemoved: any[] = [];
    fkeyStore: any[] = [];
    downloadStore: any[] = [];

    dropDownJoinTable: DropdownLevel[] = [];

    dictionary: Dictionary[] = [];
    tableNameList: any[] = [];

    sugestion: any[] = [];
    filteredSugestion: any[] = [];

    categories: any[] = [];
    filteredCategories: any[] = [];

    application: any[] = [];
    filteredAppNames: any[] = [];

    dataType: any[] = [];

    
    lastTableLazyLoadEvent! : LazyLoadEvent;
    inputForm!: FormGroup;
    inputForm2!: FormGroup;
    
    filteringAps: string = ''

    stateOptions: any[] = [
        { label: 'No', value: false },
        { label: 'Yes', value: true },
    ];
    
    constructor(
        private fb: FormBuilder,
        private api: MasterService,
        private confirmationService: ConfirmationService,
        private messageService: MessageService,
        private spinner: NgxSpinnerService
    ) {
        
    }
    ngOnInit(): void {
        this.dropdownValueInit();
        this.fieldIdRemoved = []
        this.inputForm = this.fb.group({
            tableName: ['',],
            extTableName: [''],
            isMaster: [false,],
            extName: [''],
            appName: [''],
            joinTo: [''],
            status: ['active'],
            isExisted: [''],
            field: this.fb.array([this.createFieldFormGroup()])
        });


        this.inputForm2 = this.fb.group({
            whereCond:[''],
            whereOperan:[''],
            whereValCond:[''],
            whereCond2:[''],
            whereOperan2:[''],
            whereValCond2:[''],
            orCond:[''],
            orOperand:[''],
            orValCond:[''],
            orCond2:[''],
            orOperand2:[''],
            orValCond2:[''],
            betweenCond:[''],
            betweenVal:[''],
            betweenCond2:[''],
            betweenVal2:[''],
            orderCond:[''],
            ascdesc:[''],
            skipinCond:[''],
            fetchOnlyCond:[''],
        })
    }

    get fieldControls() {
        return (this.inputForm.get('field') as FormArray).controls;
    }

    getEventValue($event:any):string{
        return $event.target.value
    }
 
    joinTableSelected($event:any){
        let a = $event.text
        this.selectedAplications = a
        // console.log(a,"????")
        this.dropDownJoinTable.unshift({
            text: 'No',
            value: '',
        });
        setTimeout(() => {
            this.api.getMaterialInput().subscribe((data: any ) => {
                this.dropDownJoinTable = data.joinTo.filter((el:any) => el.app == a)
                // console.log(this.dropDownJoinTable);
                
            },(error) => {
                console.log(error)
            })
        }, 500);
        
    }

    foreignkeySelectedTable(data: any) {
        this.api.getOneTable(data).subscribe((res) => {
            let e = res.field_data.filter((el:any) => el.statPk == '1')
            this.fkeyStore = e.map((el:any) => {
                return {"text":el.name_caption, "value":el.field_id}
            })
        },(err) => {
            console.log(err)
        })
    }
    
    foreignkeySelectedField(data: any) {
        console.log(data)
    }

    foreignKeySelection() {
        console.log(this.selectedAplications)
        if(this.selectedAplications) {
            setTimeout(() => {
                this.api.getDataFkey().subscribe((data:any) => {
                    this.fkey = data.data.filter((el:any) => el.app == this.selectedAplications)
                    console.log(this.fkey)
                },(error) => {
                    console.log(error)
                })
            }, 750);
        } else {
        }
    }

    fourCharSugestions($event:any) {
        let x = $event.text
        setTimeout(() => {
            this.api.getMaterialInput().subscribe((data: any) => {
                this.sugestion = data.sugestion.filter((el:any) => el.key == x)
            })
        }, 1000);
    }

    loadDictionary(event:LazyLoadEvent) {
        this.loading = true;
        this.lastTableLazyLoadEvent = event;
        this.sugestionInit()
        setTimeout(() => {
            const sortMethod = 'DESC'

            const param = {
                'dataPerPage' : event.rows,
                'dataBefore' : event.first,
                'orderBy' : "AAMCEATZ1302",
                'orderMethod' : sortMethod, 
                'globalFilter' :  event.globalFilter
            }

            this.api.getAllTable(param).subscribe(
                (data: any) => {
                    console.log(data)
                    let dataTable = data.result;
                    let fieldsPerTable = data.fields
                    this.tableNameList = dataTable
                    this.dictionary = dataTable.map((data:any) => {
                        let fields = fieldsPerTable.find((field:any) => field.headerId === data.id);
                        return { ...data, ...fields };
                      });
                    this.totalRecord = data.totalRecord
                    this.loading = false;
                },
                (error) => {
                    this.loading = false;
                    // this.auth.notAuthorized(error.status, error.error)
                    this.messageService.add({
                        key: 'Message',
                        severity: 'error',
                        summary: 'Reload Data',
                        detail: 'Failed',
                    });
                }
            );
        }, 5000);
    }

    sugestionInit() {
        this.spinner.show()
        this.loadSugestionInit = false
        if(this.sugestion.length <= 0 ) {
            setTimeout(() => {
                this.api.getMaterialInput().subscribe(
                    (data: any) => {
                        console.log(data)
                        this.sugestion = data.sugestion;
                        this.application = data.dropApp;
                        this.categories = data.category;
                        this.spinner.hide()
                        this.loadSugestionInit = false
                    },
                    (error) => {
                        this.spinner.hide()
                        console.log(error);
                    }
                );
            }, 1000);
        } else {
            this.loadSugestionInit = false
            this.spinner.hide()
        }
    }

    filteredSugestionInit(event: any) {
        let filtered: any[] = [];
        let query = event.query;

        for (let i = 0; i < this.sugestion.length; i++) {
            let data = this.sugestion[i];
            if (data.key.toLowerCase().indexOf(query.toLowerCase()) == 0) {
                filtered.push(data);
            }
        }

        this.filteredSugestion = filtered;
    }

    filterCategory(event: any) {
        let filtered: any[] = [];
        let query = event.query;

        for (let i = 0; i < this.categories.length; i++) {
            let data = this.categories[i];
            if (data.key.toLowerCase().indexOf(query.toLowerCase()) == 0) {
                filtered.push(data);
            }
        }

        this.filteredCategories = filtered;
    }

    filterAppName(event: any) {
        let filtered: any[] = [];
        let query = event.query;

        for (let i = 0; i < this.application.length; i++) {
            let data = this.application[i];
            if (data.text.toLowerCase().indexOf(query.toLowerCase()) == 0) {
                filtered.push(data);
            }
        }

        this.filteredAppNames = filtered;
    }

    findCategoryByValue(val: any) {
        return this.categories.find(({ value }) => value == val);
    }

    findAplicationByValue(val: any) {
        const x = this.application.find(({ text }) => text == val);
        return x
    }

    findJoinTo(val: any, app:any) {
        if(val == "None") {
            // this.inputForm.controls['joinTo'].disable();
            console.log(this.inputForm.controls['joinTo'].getRawValue())
        } else {
            // this.inputForm.controls['joinTo'].enable();
            let x = this.dropDownJoinTable.find(({value}) => value == val)
            console.log(x,x?.text)
            return x?.text
        }
    }

    findFieldNameByValue(val: any) {
        let x = this.sugestion.find(({ key }) => key == val);
        if (!x ){
            x = {"key": val}
            return x
        } else {
            return x.key
        }
    }

    findEditFieldNameByValue(val:any) {
        const zz = val.slice(0,4)
        let z = this.sugestion.find(({value}) => value == zz)
        if(!z){
            z = {"key": val}
            return z
        } else {
            return z
        }
    }

    findFieldNameByKey(key: any) {
        const s = key
        // let y = this.getId.length <= 6 ? this.getId.slice(2) : this.getId.slice(4)
        let x = this.sugestion.find(({ value }) => value == s );
        if(!x) {
            x = {'value': key}
        }
        return x
    }

    findFieldDataType(val: any) {
        const x = this.dataType
            .flatMap((item) => item.items)
            .find(({ value }) => value == val);
        return x.value;
    }

    findfieldIsPk(val: any) {
        let a = false;
        if (val === '1') {
            a = true;
        }
        const y = this.stateOptions.find(({ value }) => value === a);

        return y.value;
    }

    findisFK(val:any) {
        if(val !== "0") {
            let x = this.fkeyStore.find(({value}) => value == val)
            if(!x) {
                x = {value: val,text:val}
            }
            return x
        }
    }

    findIsFKto(val:any) {
        if(val == "0") {
            // this.inputForm.controls['joinTo'].disable();
            console.log(this.inputForm.controls['joinTo'].getRawValue())
        } else {
            // this.inputForm.controls['joinTo'].enable();
            let x = this.dropDownJoinTable.find(({value}) => value == val)
            console.log(x,x?.text)
            return x?.text
        }
    }

    dropdownValueInit() {
        this.dataType = [
            {
              label: 'Exact Numerics',
              items: [
                { label: 'bit', value: 'bit', max: '1' },
                { label: 'tinyint', value: 'tinyint', max: '255' },
                { label: 'smallint', value: 'smallint', max: '32,767' },
                { label: 'int', value: 'int', max: '2,147,483,647' },
                { label: 'bigint', value: 'bigint', max: '9,223,372,036,854,775,807' },
                { label: 'decimal', value: 'decimal', max: '38' },
                { label: 'numeric', value: 'numeric', max: '38' },
                { label: 'money', value: 'money', max: '922,337,203,685,477.5807' },
                { label: 'smallmoney', value: 'smallmoney', max: '214,748.3647' },
                { label: 'float', value: 'float', max: '1.79E+308' },
                { label: 'real', value: 'real', max: '3.40E+38' },
              ],
            },
            {
              label: 'Approximate Numerics',
              items: [
                { label: 'float', value: 'float', max: '1.79E+308' },
                { label: 'real', value: 'real', max: '3.40E+38' },
              ],
            },
            {
              label: 'Date and Time',
              items: [
                { label: 'date', value: 'date', max: '9999-12-31' },
                { label: 'time', value: 'time', max: '23:59:59.9999999' },
                { label: 'datetime', value: 'datetime', max: '9999-12-31 23:59:59.997' },
                { label: 'datetime2', value: 'datetime2', max: '9999-12-31 23:59:59.9999999' },
                { label: 'smalldatetime', value: 'smalldatetime', max: '2079-06-06 23:59:00' },
                { label: 'datetimeoffset', value: 'datetimeoffset', max: '9999-12-31 23:59:59.9999999 +14:00' },
              ],
            },
            {
              label: 'Character Strings',
              items: [
                { label: 'char', value: 'char', max: '8,000' },
                { label: 'varchar', value: 'varchar', max: '8,000' },
                { label: 'text', value: 'text', max: '2^31-1' },
                { label: 'nchar', value: 'nchar', max: '4,000' },
                { label: 'nvarchar', value: 'nvarchar', max: '4,000' },
                { label: 'ntext', value: 'ntext', max: '2^30-1' },
              ],
            },
            {
              label: 'Binary Strings',
              items: [
                { label: 'binary', value: 'binary', max: '8,000' },
                { label: 'varbinary', value: 'varbinary', max: '8,000' },
                { label: 'image', value: 'image', max: '2^31-1' },
              ],
            },
            // {
            //   label: 'Other Data Types',
            //   items: [
            //     { label: 'uniqueidentifier', value: 'uniqueidentifier', max: 'Guid' },
            //     { label: 'xml', value: 'xml', max: '2^31-1' },
            //     { label: 'cursor', value: 'cursor', max: '-' },
            //     { label: 'table', value: 'table', max: '-' },
            //     { label: 'variant', value: 'variant', max: '-' },
            //     { label: 'sql_variant', value: 'sql_variant', max: '-' },
            //   ],
            // },
          ];
    }

    showForm() {
        this.sugestionInit()
        this.isEdit = false;
        this.isExistingTable = false
        this.inputForm.controls['tableName'].enable();
        this.inputForm.controls['joinTo'].enable();
        this.modalTitle = 'Create a new Table';
        this.inputForm.reset();
        this.displayForm = true;
        const fieldArr = this.inputForm.get('field') as FormArray;
        fieldArr.clear();
    }

    existingTableForm() {
        this.sugestionInit()
        this.isEdit = false;
        this.isExistingTable = true
        this.inputForm.controls['tableName'].enable();
        this.modalTitle = 'Insert an Existing Table';
        this.inputForm.reset();
        this.displayForm = true;
        const fieldArr = this.inputForm.get('field') as FormArray;
        fieldArr.clear();
    }

    showEditForm(data: any) {
        this.sugestionInit()
        this.isEdit = true;
        this.isExistingTable = false
        this.modalTitle = `Edit ${data.isExisting == "1" ? "Existing Table": "Table"} ${data.id}`;
        this.editExistingTable = data.isExisting == "1" ? true : false;
        this.displayForm = true;
        this.inputForm.controls['tableName'].disable();
        this.getId = data.id;
        this.editableDatas.push(data)
        
        // console.log(this.editableDatas)
        // console.log(data, "INI")
        this.fieldIdRemoved = []
        
        this.api.getOneTable(data.id).subscribe(
            (res) => {
                console.log(res)
                let appName = res.table_data.aplication_name
                let obj = {text:appName}
                console.log(res.field_data.length)
                let countField = res.field_data.length
                let stopCount = 0
                // let stoped = false
                for(let is = 0;is < countField ;is++) {
                    const fieldArray = this.inputForm.get('field') as FormArray;
                    fieldArray.push(this.createFieldFormGroup());
                    stopCount += 1
                }
                if(countField == stopCount) {
                    this.joinTableSelected(obj)
                    this.editTableDetail = res.field_data.map((el: any,i:number) => {
                        return {
                            fieldNameEdit: this.findEditFieldNameByValue(el.field_id),
                            fieldName: this.findFieldNameByKey(el.field_id),
                            extFname: this.findFieldNameByValue(el.name_caption),
                            maxLenValue: el.default_value,
                            datTypeField: el.data_type.toLowerCase(),
                            isPk: this.findfieldIsPk(el.statPk),
                            // statTD: el.status !== "0" ? el.status:"",
                            isFK: el.isFK !== "0" ? this.findisFK(el.isFK) : "",
                            isFKto: el.isFKto !== "0" ? this.findIsFKto(el.isFKto) : ""//debuging disini besok!!!
                        };
                    });
                    // console.log(this.fieldIdRemoved,"chek rubah sebelum hapus")
                    this.inputForm.patchValue({
                        tableName: res.table_data[0].caption_table,
                        appName: this.findAplicationByValue(
                            res.table_data[0].aplication_name
                        ),
                        isMaster: this.findCategoryByValue(
                            res.table_data[0].kategori_app
                        ),
                        joinTo: res.table_data[0].joinTo,
                        isExisted: res.table_data[0].isExist,
                        field: this.editTableDetail,
                    });
                    const fieldArr = this.inputForm.get('field') as FormArray;
                    fieldArr.clear();
                    this.editTableDetail.forEach((field) => {
                        fieldArr.push(this.createFieldControl(field));
                    });
                }
            },
            (err) => {
                console.log(err);
            }
        );
    }

    showQuery() {
        const userInput = this.inputForm.getRawValue();
        console.log(userInput)
        console.log(this.fkeyStore)
        if (this.inputForm.invalid) {
            this.messageService.add({
                key: 'Message',
                severity: 'error',
                summary: 'Submit Form',
                detail: 'Failed, there is empty data',
            });
            return;
        } else {
            if (this.isEdit == true) {
                this.loading = true
                
                this.api.editPreviewQuery(userInput, this.getId).subscribe(
                    (res) => {
                        this.loading = false
                        this.displayQuery = res.queries;
                        console.log(res)
                    },
                    (err) => {
                        console.log(err);
                        this.isLoadingButton = false
                    }
                );
                
            } 
            else if(this.isExistingTable == true) {
                this.api.postPreviewExtQuery(userInput).subscribe((res) => {
                    console.log(res)
                        let temp = res.split('?');
                        for (let i = 1; i < temp.length - 2; i++) {
                            let values = this.checkParse(temp[i])
                            temp[i] = values + ','
                        }
                        this.displayQuery = temp.join("")
                },(err) => {
                    console.log(err)
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Failed',
                        detail: 'Gagal Generate Query!',
                    });
                    this.isLoadingButton = false
                })
            }
            if(this.isExistingTable !== true && this.isEdit !== true) {
                this.api.postPreviewQuery(userInput).subscribe(
                    (res) => {
                        console.log(res)
                        let temp = res.split('?');

                        for (let i = 1; i < temp.length - 2; i++) {
                            let values = this.checkParse(temp[i])
                            temp[i] = values + ','
                        }
                        this.displayQuery = temp.join("")
                    },
                    (err) => {
                        console.log(err)
                        this.isLoadingButton = false
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Failed',
                            detail: 'Gagal Generate Query!',
                        });
                    }
                );
            }
        }
        
        setTimeout(() => {
            this.confirmationService.confirm({
                header: 'Preview Query',
                message: this.displayQuery,
                icon: 'pi pi-server',
                accept: () => {
                    this.submitForm();
                    this.messageService.add({
                        severity: 'info',
                        summary: 'Confirmed',
                        detail: 'You have accepted',
                    });
                },
                reject: (type: any) => {
                    this.isLoadingButton = false
                    this.loading = false
                    switch (type) {
                        case ConfirmEventType.REJECT:
                            this.messageService.add({
                                severity: 'error',
                                summary: 'Rejected',
                                detail: 'You have rejected',
                            });
                            break;
                        case ConfirmEventType.CANCEL:
                            this.messageService.add({
                                severity: 'warn',
                                summary: 'Cancelled',
                                detail: 'You have cancelled',
                            });
                            break;
                    }
                },
            });
        }, 500);
    }

    createFieldControl(field: any): FormGroup {
        return this.fb.group({
            fieldNameEdit: [field.fieldNameEdit],
            extFname: [field.extFname],
            fieldName: [field.fieldName],
            maxlenField: [Number(field.maxLenValue)],
            datTypeField: [field.datTypeField],
            isPk: [field.isPk],
            statTD:[field.statTD]
        });
    }

    createFieldFormGroup() {
        return this.fb.group({
            fieldNameEdit:[''],
            extFname:[''],
            fieldName: [''],
            datTypeField: ['', Validators.required],
            maxlenField: [0],
            isPk: [false],
            isFK:[''],
            isFKto:[''],
            statTD:['active']
        });
    }

    setStatTD(index:number,value:string) {
        console.log('clicked should be change field status from field no = ', index ,"changing value to ", value)
        const fieldCont = this.inputForm.get('field') as FormArray;
        const fieldG = fieldCont.at(index) as FormGroup;
        const statChange = fieldG.get('statTD')
        statChange?.setValue(value)
    }

    togleStatusField(data:any,i:any) {
        console.log(data,i, 'togle status')
        if(data == 'active') {
            this.blockedFields[i] = false
            console.log("Not Blocked")
            
        } else {
            this.blockedFields[i] = true
            console.log("Blocked")
            
        }
        
    }

    addField() {
        console.log("clicked")
        const fieldArray = this.inputForm.get('field') as FormArray;
        fieldArray.push(this.createFieldFormGroup());        
        const newFieldElement = document.getElementById('bawah');        
        if (newFieldElement) {
          newFieldElement.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'end' });
        }
    }

    toTop(){
        const targetTo = document.getElementById('toButtonAdd');        
        if (targetTo) {
          targetTo.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'end' });
        }
    }
    
    undoDeleteField(index: number) {
        if (this.fieldIdRemoved.length > 0) {
            const fieldArray = this.inputForm.get('field') as FormArray;
            const a = fieldArray.at(index).getRawValue();
            const fieldNameValue = a.fieldName.value;

            if(this.fieldIdRemoved.includes(fieldNameValue)) {
                let w = this.fieldIdRemoved.indexOf(fieldNameValue)
                this.fieldIdRemoved.splice(w, 1,'XXXX');
                this.fieldStatus = false
                this.blockedFields[index] = false
                console.log(this.editableDatas,this.fieldStatus, "UNDO")
                this.messageService.add({
                    key: 'Message',
                    severity: 'success',
                    summary: "Undo Field Deleted",
                    detail: "Field Id Removed from deleted list!",
                });
            } else {
                console.log("No fields to undo deletion.");
                this.messageService.add({
                    key: 'Message',
                    severity: 'error',
                    summary: "Failed",
                    detail: "No fields to undo deletion.",
                });
            }
        } else {
            console.log("No fields to undo deletion.");
            this.messageService.add({
                key: 'Message',
                severity: 'error',
                summary: "Failed",
                detail: "No fields to undo deletion.",
            });
        }
        console.log(this.fieldIdRemoved)
    }

    removeField(index: number) {
        const fieldArray = this.inputForm.get('field') as FormArray;
        if(this.isEdit) {
            if(fieldArray.length  <= this.editableDatas[this.editableDatas.length-1].totalField){
                console.log('cannot remove')
                this.messageService.add({
                    key: 'Message',
                    severity: 'error',
                    summary: "Delete Field Error",
                    detail: "This Input Form Field contain Data that cannot be Deleted!",
                });
            }else {
                console.log("remove")
                fieldArray.removeAt(index)
            }
        }else {
            console.log("remove input")
            fieldArray.removeAt(index)
        }
        // fieldArray.removeAt(index) 
        console.log(fieldArray.length <= this.editableDatas[this.editableDatas.length-1].totalField)
        console.log(fieldArray.length,this.editableDatas[this.editableDatas.length-1].totalField,this.isEdit,this.editExistingTable)
    }
    
    deleteField(index: number) {
        const fieldArray = this.inputForm.get('field') as FormArray;
        
        const a = fieldArray.at(index).getRawValue();
        const fieldNameValue = a.fieldName.value;
        // debuging penempatan value ke array agar sesuai dengan undo!!!
        for(let i = 0 ; i < this.editableDatas[this.editableDatas.length-1].totalField ; i++) {
            const v = 'XXXX'
            this.fieldIdRemoved.push(v)
        }

        if(this.fieldIdRemoved.length > this.editableDatas[this.editableDatas.length-1].totalField) {
            this.fieldIdRemoved = this.fieldIdRemoved.slice(0, this.editableDatas[this.editableDatas.length-1].totalField)
        }

        console.log(this.fieldIdRemoved,fieldArray.controls.length)
        if (!this.fieldIdRemoved.includes(fieldNameValue) && fieldNameValue !== undefined) {
          this.fieldIdRemoved.splice(index, 1 , fieldNameValue);
          console.log(index, 1 , fieldNameValue)
          this.fieldStatus = true
          this.blockedFields[index] = true
          this.messageService.add({
            key: 'Message',
            severity: 'success',
            summary: "Field Deleted",
            detail: "Field Id Added to deleted list! this will work after submited!",
            });
          console.log("Field Id Added to deleted list! this will work after submited!");
        } else {
            console.log(!this.fieldIdRemoved.includes(fieldNameValue) && fieldNameValue !== undefined)
            this.messageService.add({
                key: 'Message',
                severity: 'error',
                summary: "Delete Field Error",
                detail: 'Field already Deleted! or Empty Field Cannot Be Deleted!',
            });
            // this.blockedFields[index] = false
            console.log("Field already exists in fieldIdRemoved. Skipping addition.");
        }
        console.log(this.fieldIdRemoved,'>> JIKA SUKSES MENAMBAHKAN ID KE LIST UNTUK DI HAPUS!',this.fieldStatus);
        
    }

    submitForm() {
        this.inputForm.patchValue({
            rmList:this.fieldIdRemoved
        })
        const userInput = this.inputForm.getRawValue();
        if (this.inputForm.invalid) {
            this.messageService.add({
                key: 'Message',
                severity: 'error',
                summary: 'Submit Form',
                detail: 'Failed, there is empty data',
            });
        } else {
            this.isLoadingButton = true;
            if(this.editExistingTable == true && this.isEdit == true){
                setTimeout(() => {
                    console.log("EDIT TABLE EXISTING")
                    console.log(this.fieldIdRemoved)
                    this.api.putSelectedExtTable(userInput, this.getId).subscribe((res) => {
                        this.displayForm = false;
                        this.fieldIdRemoved = []
                            this.loadDictionary(this.lastTableLazyLoadEvent);
                            this.messageService.add({
                                key: 'Message',
                                severity: 'success',
                                summary: 'Edit Table',
                                detail: 'Successful',
                            });
                            this.isLoadingButton = false;
                            this.sugestionInit()
                    },(err) => {
                        this.messageService.add({
                            key: 'Message',
                            severity: 'error',
                            summary: 'Edit Table',
                            detail: 'failed',
                        });
                        this.isLoadingButton = false;
                    })                    
                }, 2000);
            }
            else if (this.isEdit && !this.editExistingTable) {
                setTimeout(() => {
                    console.log("EDIT TABLE MASTER")
                    console.log(this.fieldIdRemoved)
                    this.api.putSelectedTable(userInput, this.getId).subscribe(
                        (res) => {
                            this.displayForm = false;
                            this.fieldIdRemoved = []
                            this.loadDictionary(this.lastTableLazyLoadEvent);
                            this.messageService.add({
                                key: 'Message',
                                severity: 'success',
                                summary: 'Edit Table',
                                detail: 'Successful',
                            });
                            this.isLoadingButton = false;
                            this.sugestionInit()
                        },
                        (err) => {
                            // this.auth.notAuthorized(error.status, error.error)
                            this.messageService.add({
                                key: 'Message',
                                severity: 'error',
                                summary: 'Edit Table',
                                detail: 'failed',
                            });
                            this.isLoadingButton = false;
                        }
                    );
                }, 2000);
            } 
            if(this.isExistingTable) {
                setTimeout(() => {
                    this.api.postExtTable(userInput).subscribe((res) => {
                        this.displayForm = false;
                        this.loadDictionary(this.lastTableLazyLoadEvent);
    
                            this.messageService.add({
                                key: 'Message',
                                severity: 'success',
                                summary: 'Data Tabel Bertambah!',
                                detail: 'Successful',
                            });
                            this.isLoadingButton = false;
                            this.sugestionInit()
                    },
                    (error) => {
                        console.log(error);
                        this.displayForm = true;
                        this.isLoadingButton = false;
                        this.messageService.add({
                            key: 'Message',
                            severity: 'error',
                            summary: 'Gagal buat table baru!',
                            detail: 'failed',
                        });
                    })                    
                }, 2000);
            }
            if(this.isExistingTable !== true && this.isEdit !== true) {
                setTimeout(() => {
                    this.api.postCreateTable(userInput).subscribe(
                        (res) => {
                            this.displayForm = false;
                            this.loadDictionary(this.lastTableLazyLoadEvent);
      
                                this.messageService.add({
                                    key: 'Message',
                                    severity: 'success',
                                    summary: 'Data Tabel Bertambah!',
                                    detail: 'Successful',
                                });
                                this.isLoadingButton = false;
                                this.sugestionInit()
                        },
                        (error) => {
                            console.log(error);
                            this.displayForm = true;
                            this.isLoadingButton = false;
                            this.messageService.add({
                                key: 'Message',
                                severity: 'error',
                                summary: 'Gagal buat table baru!',
                                detail: 'failed',
                            });
                        }
                    );
                }, 1000);
            }
        }
    }

    deleteBtn(data: any, event: any) {
        this.loading = true;
        this.confirmationService.confirm({
            target: event.target,
            message: 'Hapus Data Table ?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.loading = true;
                const id = data.id;
                this.api.updateStatusTable(id).subscribe(
                    (res) => {
                        console.log(res)
                        this.loading = false;
                        this.loadDictionary(this.lastTableLazyLoadEvent);
                    },
                    (err) => {
                        console.log(err);
                        this.loadDictionary(this.lastTableLazyLoadEvent);
                        this.loading = false;
                    }
                );
            },
            reject: () => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Rejected',
                    detail: 'You have rejected',
                });
                this.loading = false;
            },
        });
    }

    viewOneQueries(data: any) {
        this.settingsQueryPlayGround()
        this.displayQuerySelect = []
        this.modalTitle = 'Generated Queries';
        this.displayOneQuery = true;
        this.api.getOneTable(data.id).subscribe(
            (res) => {
                console.log(res)
                this.displayQueryAfter = res.createdQuery.split('?');
                for (let i = 1; i < this.displayQueryAfter.length - 3; i++) {
                    let values = this.checkParse(this.displayQueryAfter[i])
                    this.displayQueryAfter[i] = values + ',';
                }

                this.displayQuerySelect = res.selecQuery.split('?');
                for (let i = 1; i < this.displayQuerySelect.length - 3; i++) {
                    let values = this.checkParse(this.displayQuerySelect[i])
                    this.displayQuerySelect[i] = values + ',';
                }

                this.columnNameList = res.field_data.map((el:any) => {
                    return {"label":el.name_caption, 'name':el.field_id}
                })

                this.selectAorDESC = [
                    {"label":"Ascending", 'value':"ASC"},
                    {"label":"Descending","value":"DESC"}
                ]

                this.whereOperandList = [
                    {"name":"=" ,	"label":"Equal to"},
                    {"name":">" ,	"label":"Greater than"},
                    {"name":"<" ,	"label":"Less than"},
                    {"name":">=" ,	"label":"Greater than or equal to"},
                    {"name":"<=" , "label":"Less than or equal to"},
                    {"name":"<>" ,	"label":"Not equal to"}
                ]

                this.orOperanList = [
                    {"name":">=" ,	"label":"Greater than or equal to"},
                    {"name":"<=" , "label":"Less than or equal to"},
                    {"name":"=" ,	"label":"Equal to"},
                    {"label":"LIKE","name":"LIKE"}
                ]
                this.selectQueryPlayGround()
            },
            (err) => {
                console.log(err);
            }
        );
    }

    selectQueryPlayGround() {
        let ui = this.inputForm2.getRawValue()
        if(!this.disableWhere && ui.whereCond) {
            this.displayQuerySelect.push(`WHERE ${ui.whereCond.name} ${ui.whereOperan.name}'${ui.whereValCond}'`)
            if(ui.whereCond2) {
                this.displayQuerySelect.push(`AND ${ui.whereCond2.name} ${ui.whereOperan2.name}'${ui.whereValCond2}'`)
            }
        }
        if(!this.disableOr && ui.orCond) {            
            if(ui.orOperand.name === 'LIKE') {
                this.displayQuerySelect.push(`OR ${ui.orCond.name} ${ui.orOperand.name} '%${ui.orValCond}%'`)
                if(ui.orOperand2) {
                    this.displayQuerySelect.push(`AND ${ui.orCond2.name} ${ui.orOperand2.name} '${ui.orValCond2}'`)
                    if(ui.orValCond2.name === 'LIKE') {
                        this.displayQuerySelect.push(`AND ${ui.orCond2.name} ${ui.orOperand2.name} '%${ui.orValCond2}%'`)
                    }
                } 
            } else {
                this.displayQuerySelect.push(`OR ${ui.orCond.name} ${ui.orOperand.name} '${ui.orValCond}'`)
            }
            
        }
        if(!this.disableBetween && ui.betweenVal) {
            this.displayQuerySelect.push(`BETWEEN ${ui.betweenCond.name} = '${ui.betweenVal}'`)
            this.displayQuerySelect.push(`AND ${ui.betweenCond2.name} = '${ui.betweenVal2}'`)
        }
        if(!this.disableOrderBy && ui.orderCond) {
            this.displayQuerySelect.push(`ORDER BY ${ui.orderCond.name} ${ui.ascdesc}`)
        }
        if(!this.disableSkipRows && ui.skipinCond && ui.fetchOnlyCond) {
            this.displayQuerySelect.push(`OFFSET ${ui.skipinCond} ROWS`)
            this.displayQuerySelect.push(`FETCH FIRST ${ui.fetchOnlyCond} ROWS ONLY`)
        }
        console.log(this.displayQuerySelect)
    }

    settingsQueryPlayGround() {
        this.loadSelectQuery = false
        this.inputForm2.reset()
        this.inputForm2.get('whereCond')?.enable()
        this.inputForm2.get('whereOperan')?.enable()
        this.inputForm2.get('whereValCond')?.enable()
        this.inputForm2.get('whereCond2')?.enable()
        this.inputForm2.get('whereOperan2')?.enable()
        this.inputForm2.get('whereValCond2')?.enable()
        this.inputForm2.get('orCond')?.enable()
        this.inputForm2.get('orCond2')?.enable()
        this.inputForm2.get('orOperand')?.enable()
        this.inputForm2.get('orOperand2')?.enable()
        this.inputForm2.get('orValCond')?.enable()
        this.inputForm2.get('orValCond2')?.enable()
        this.inputForm2.get('betweenCond')?.enable()
        this.inputForm2.get('betweenCond2')?.enable()
        this.inputForm2.get('betweenVal')?.enable()
        this.inputForm2.get('betweenVal2')?.enable()
        this.inputForm2.get('orderCond')?.enable()
        this.inputForm2.get('ascdesc')?.enable()
        this.inputForm2.get('skipinCond')?.enable()
        this.inputForm2.get('fetchOnlyCond')?.enable()
        this.disableWhere = false
        this.disableOr = false
        this.disableBetween = false
        this.disableOrderBy = false
        this.disableSkipRows = false
        this.disableFetchOnly = false
    }

    caseSwitch() {
        if(this.disableWhere) {
            this.inputForm2.get('whereCond')?.disable()
            this.inputForm2.get('whereOperan')?.disable()
            this.inputForm2.get('whereValCond')?.disable()
            this.inputForm2.get('whereCond2')?.disable()
            this.inputForm2.get('whereOperan2')?.disable()
            this.inputForm2.get('whereValCond2')?.disable()
        } else {
            this.inputForm2.get('whereCond')?.enable()
            this.inputForm2.get('whereOperan')?.enable()
            this.inputForm2.get('whereValCond')?.enable()
            this.inputForm2.get('whereCond2')?.enable()
            this.inputForm2.get('whereOperan2')?.enable()
            this.inputForm2.get('whereValCond2')?.enable()
        }

        if(this.disableOr) {
            this.inputForm2.get('orCond')?.disable()
            this.inputForm2.get('orCond2')?.disable()
            this.inputForm2.get('orOperand')?.disable()
            this.inputForm2.get('orOperand2')?.disable()
            this.inputForm2.get('orValCond')?.disable()
            this.inputForm2.get('orValCond2')?.disable()
            
        } else {
            this.inputForm2.get('orCond')?.enable()
            this.inputForm2.get('orCond2')?.enable()
            this.inputForm2.get('orOperand')?.enable()
            this.inputForm2.get('orOperand2')?.enable()
            this.inputForm2.get('orValCond')?.enable()
            this.inputForm2.get('orValCond2')?.enable()
        }

        if(this.disableBetween) {
            this.inputForm2.get('betweenCond')?.disable()
            this.inputForm2.get('betweenCond2')?.disable()
            this.inputForm2.get('betweenVal')?.disable()
            this.inputForm2.get('betweenVal2')?.disable()
        } else {
            this.inputForm2.get('betweenCond')?.enable()
            this.inputForm2.get('betweenCond2')?.enable()
            this.inputForm2.get('betweenVal')?.enable()
            this.inputForm2.get('betweenVal2')?.enable()
        }

        if(this.disableOrderBy) {
            this.inputForm2.get('orderCond')?.disable()
            this.inputForm2.get('ascdesc')?.disable()
        } else {
            this.inputForm2.get('orderCond')?.enable()
            this.inputForm2.get('ascdesc')?.enable()
        }

        if(this.disableSkipRows) {
            this.inputForm2.get('skipinCond')?.disable()
            this.inputForm2.get('fetchOnlyCond')?.disable()
        } else {
            this.inputForm2.get('skipinCond')?.enable()
            this.inputForm2.get('fetchOnlyCond')?.enable()
        }
    }

    checkParse(val: any) {
        if(val[0] == "{"){
            let a = val.slice(11,19)
            let b = val.slice(21)
            return a + b
        } else {
            return val
        }
    }

    defEksisting(val:any) {
        if(val == 0) {
            return 'From Master'
        } else {
            return 'From Existing Table'
        }
    }
    
    defJoined(val:any) {
        if(val == 'None') {
            return 'Not Join to any Table'
        } else {
            return `Joined with Table ${val}`
        }
    }

    getDatTypeValidator(event:any) {
        console.log(event.value,"DATA TYPE FIELD")
        const val = event.value
        let data = this.dataType.map((obj) => ({
            label: obj.label,
            items: obj.items.find((item:any) => item.value === val),
          }))
        let filteredItems = data.filter((el:any) => el.items !== undefined)
        if(filteredItems[0].label == "Exact Numerics" && filteredItems[0].items.value == val){
            if(filteredItems[0].items.value == 'float' || filteredItems[0].items.value == 'real'){
                this.maxLenValidator = parseFloat(filteredItems[0].items.max)
                console.log(this.maxLenValidator,"Float Condition")
            }else {
                this.maxLenValidator = parseInt((filteredItems[0].items.max).replace(/,/g,""),10)
                console.log(this.maxLenValidator,"Not Float Condition")
            }
        } else if(filteredItems[0].label == "Approximate Numerics" && filteredItems[0].items.value == val) {
            this.maxLenValidator = parseFloat(filteredItems[0].items.max)
                console.log(this.maxLenValidator,"Float Condition Approx")
        } else if(filteredItems[0].label == "Date and Time" && filteredItems[0].items.value == val) {
            if(filteredItems[0].items.value == 'time'){
                this.maxLenValidator = Math.round(Number(filteredItems[0].items.max.split(":").join("")))
                console.log(this.maxLenValidator,"Time Condition")
            } else {
                this.maxLenValidator = Date.parse(filteredItems[0].items.max)
                    console.log(this.maxLenValidator,"Date Condition")
            }
        } else if(filteredItems[0].label == "Character Strings" && filteredItems[0].items.value == val) {
            if(filteredItems[0].items.value == 'text' || filteredItems[0].items.value == 'ntext'){
                const inputString = filteredItems[0].items.max;
                const parts = inputString.split("^"); 
                const base = parseInt(parts[0]); 
                const exponent = parseInt(parts[1].split("-")[0]); 
                const result = Math.pow(base, exponent) - 1; 
                this.maxLenValidator = result
                console.log(this.maxLenValidator,"Text Condition")
            }else {
                this.maxLenValidator = parseInt((filteredItems[0].items.max).replace(/,/g,""),10)
                console.log(this.maxLenValidator,"Normal Condition")
            }
        }else if(filteredItems[0].label == "'Binary Strings'" && filteredItems[0].items.value == val) {
            if(filteredItems[0].items.value == 'image'){
                const inputString = filteredItems[0].items.max;
                const parts = inputString.split("^"); 
                const base = parseInt(parts[0]); 
                const exponent = parseInt(parts[1].split("-")[0]); 
                const result = Math.pow(base, exponent) - 1; 
                this.maxLenValidator = result
                console.log(this.maxLenValidator,"Text Condition")
            }else {
                this.maxLenValidator = parseInt((filteredItems[0].items.max).replace(/,/g,""),10)
                console.log(this.maxLenValidator,"Normal Condition")
            }
        }
    }

    sendToDownloadPage(data:any) {
        data.map((el:any) => {
            this.downloadStore.push(el)
        })
        this.totalStoredQuery += 1
    }

    downloadQueries(){
        console.log("clicked download");
        this.api.downloadQuerries(this.downloadStore).subscribe((res) => {
            console.log("berhasil Kirim Data")
            console.log(res)
            if(res.msg == "No Data!"){
                console.log("ERROR NO DATA INSERTED!")
                this.messageService.add({
                    key: 'Message',
                    severity: 'error',
                    summary: 'No Data!',
                    detail: 'Failed, send an empty data!',
                });
                this.downloadQuery = false
                // this.downloadLink = res.download_url; // Ambil URL download dari respons API

                return 
            }
            this.createdFileName = res.fileName
            this.readyToDownloads = true
            this.totalStoredQuery = 0
            this.downloadStore = []
        },(err) => {
            console.log("gagal download")
        })
    }

    getDownloadQueries(){
        let obj = {
            param: this.createdFileName
        }
        this.api.getDownloadQuerries(obj).subscribe((res) => {
            console.log(res)
            this.totalStoredQuery = 0
            this.downloadStore = []
            this.downloadQuery = false
            this.readyToDownloads = false
            setTimeout(() => {
                this.api.deleteAfterDownloads(obj).subscribe((res) => {
                    console.log(res)
                    this.createdFileName = ''
                    this.messageService.add({
                        key: 'Message',
                        severity: 'success',
                        summary: 'Download success!',
                        detail: `downloaded!`,
                    });
                },(err) => {
                    console.log(err)
                })
            }, 500);
        },(err) => {
            console.log(err)
            this.messageService.add({
                key: 'Message',
                severity: 'error',
                summary: 'Download Failed!',
                detail: `Failed, ${err.statusText}!`,
            });
            this.totalStoredQuery = 0
            this.downloadStore = []
            this.downloadQuery = false
            this.readyToDownloads = false
            setTimeout(() => {
                this.api.deleteAfterDownloads(obj).subscribe((res) => {
                    console.log(res)
                    this.createdFileName = ''
                },(err) => {
                    console.log(err)
                })
            }, 500);
        })
    }
}
