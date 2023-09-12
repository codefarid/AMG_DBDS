import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import {
    LazyLoadEvent,
    MessageService,
    ConfirmationService,
    ConfirmEventType,
    MenuItem,
} from 'primeng/api';
import { MasterService } from 'src/app/service/master.service';
import { DropdownLevel } from 'src/app/_model/dropdown-value.model';

@Component({
    selector: 'app-add-def',
    templateUrl: './add-def.component.html',
    styleUrls: ['./add-def.component.scss'],
})
export class AddDefComponent implements OnInit {
    loading = false;

    selectedTable: any[] = [];
    tableOptions: any[] = [];
    applications: DropdownLevel[] = []
    idTable: any;
    textTable:any;
    filteringApps: any;

    inputForm!: FormGroup;
    constructor(
        private fb: FormBuilder,
        private api: MasterService,
        private confirmationService: ConfirmationService,
        private messageService: MessageService
    ) {}

    ngOnInit() {
      this.api.getTableAndFields().subscribe((res:any) => {
       this.applications = res.app.map((el:any) => {
        return {
          text: el.text,
          value: el.text
        }
       })
        // console.log(res:any)
      }, (err:any) => {
        // console.log(err)
        this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Fetch Definition" , detail: err.message })
        
      })
    }

    fetchTableData(id:string) {
      // console.log(id)
      this.api.getDetailedFields(id).subscribe((res:any) => {
        // console.log(res:any)
        this.selectedTable = res.fields
      }, (err:any) => {
        // console.log(err)
        this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Fetch Definition" , detail: err.message })
      })
      
    }

    onChangeTable(event:any) {
      this.idTable = event.value
      this.fetchTableData(this.idTable)
    }

    onChangeApp(event:any) {
      this.filteringApps = event.value
      // console.log(this.filteringApps)
      this.api.getTableAndFields().subscribe((res:any) => {
        // console.log(res.tables.filter((el:any) => el.app == this.filteringApps))
        let catDict = [{value:'1', text:'Master'},{value:'2', text:'Transaction'},{value:'3', text:'Record'}]
        let a = res.tables.filter((el:any) => el.app == this.filteringApps)
        let result = catDict.map(category => {
          return {
            label: category.text,
            value: category.value,
            items: a.filter((item:any) => item.categories === category.value)
              .map((item:any )=> {
                return {
                  headerId: item.headerId,
                  tableName: item.tableName
                };
              })
          };
        });
        // console.log(result)
        // this.tableOptions = res.tables.filter((el:any) => el.app == this.filteringApps)
        this.tableOptions = result
       }, (err:any) => {
        //  console.log(err)
         this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Fetch Definition" , detail: err.message })
       })
    }

    displayPk(string:any) {
      const x = string == "1" ? "Yes" : "No";
      return x
    }
}
