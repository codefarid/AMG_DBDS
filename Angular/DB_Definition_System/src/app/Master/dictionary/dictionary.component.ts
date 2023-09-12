import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { LazyLoadEvent, MessageService, ConfirmationService, ConfirmEventType, MenuItem } from 'primeng/api';
import { MasterService } from 'src/app/service/master.service';

@Component({
  selector: 'app-dictionary',
  templateUrl: './dictionary.component.html',
  styleUrls: ['./dictionary.component.scss']
})
export class DictionaryComponent implements OnInit {
  loading = false
  totalRecord = 0
  modalTitle = "New Dictionary"
  
  displayForm = false
  isEdit = false
  getId  = ''
  
  
  dictionaries: any[] = [];
  stateOptions: any[] = [
    { label: 'Off', value: 'inactive' },
    { label: 'On', value: 'active',selected:'true' }
    ];
    
  lastTableLazyLoadEvent! : LazyLoadEvent
  inputForm!: FormGroup
  
  constructor(private fb: FormBuilder, private api: MasterService, private confirmationService: ConfirmationService, private messageService: MessageService) {
    
  }

  ngOnInit(): void {
    this.createForm()
  }

  getEventValue($event:any):string{
    return $event.target.value
  }

  togleStatusEdit(val:any) {
    if(val == "None"){
      let y = 'inactive'
      return y
    } else {
      if(val == 'on') {
        val = 'active'
      }
      const x = this.stateOptions.find(({ value }) => value === val);
      return x.value
    }
  }

  loadDictionaries(event: LazyLoadEvent) {
    this.loading = true;
    this.lastTableLazyLoadEvent = event;

    setTimeout(() => {
      const sortMethod = event.sortOrder==1?'ASC':'DESC'

      const param = {
        'dataPerPage' : event.rows,
        'dataBefore' : event.first,
        'orderBy' : event.sortField,
        'orderMethod' : sortMethod, 
        'globalFilter' :  event.globalFilter
      }
    
      this.api.getDictionaries(param).subscribe(
        data => {
          this.loading = false
          this.dictionaries = data['result']
          this.totalRecord = data['totalRecord']
        },
        error => {
          this.loading = false;
          // this.auth.notAuthorized(error.status, error.error)
        }
      )
      
          // this.loading = false;
      }, 1000);
  }

  createForm(){
    this.inputForm = this.fb.group({
      code: ['', Validators.required],
      value: ['', Validators.required],
      stat: ['active',Validators.required]
    });
  }

  showForm() {
    this.isEdit = false;
    this.modalTitle = 'Create a New Dictionary Sugestions';
    this.inputForm.reset()
    this.inputForm.controls['code'].enable();
    this.inputForm.controls['value'].enable();
    this.inputForm.controls['stat'].setValue('on')
    this.displayForm = true;
  }
  showEditForm(data:any) {
    this.isEdit = true;
    this.modalTitle = 'Edit Categories';
    this.displayForm = true;
    this.inputForm.controls['code'].disable();
    this.inputForm.controls['value'].disable()
    this.getId = data.code
    
    this.api.getOneDictionaries(this.getId).subscribe((res) => {
      
      const d = res.result[0]
      // console.log(d);
      
      this.inputForm.patchValue({
        code: d.code,
        value: d.value,
        stat: this.togleStatusEdit(d.status)
      })
    }, (err) => {
      // console.log(err)
    })
        
  }

  submitForm() {
    const userInput = this.inputForm.getRawValue()
    this.inputForm.controls['code'].value.toUpperCase()
    if (this.inputForm.invalid) {
      this.messageService.add({ key: 'Message', severity: 'error', summary: 'Submit Form', detail: 'Failed, there is empty data' })
    } else {
      if(this.isEdit) {
        this.api.putDictionaries(userInput, this.getId).subscribe((res) => {
          // console.log(res)
          if(res.message == "Nama Sudah Ada, Buat Nama lain!") {
            this.messageService.add({ key: 'Message', severity: 'error', summary: res.message , detail: 'Failed' })
            this.displayForm = true
          } else {
            this.loadDictionaries(this.lastTableLazyLoadEvent)
            this.displayForm = false
            this.messageService.add({ key: 'Message', severity: 'success', summary: "Success Edit Dictionary" , detail: 'Successful' })
          }
          
         }, (err) => {
          // console.log(err)
          this.displayForm = true
          this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Edit Dictionary" , detail: 'Failed' })
          // console.log(err)
        })
      } else {
        this.api.postDictionaries(userInput).subscribe((res) => {
          
          if(res.message == "Nama Sudah Ada, Buat Nama lain!") {
            this.messageService.add({ key: 'Message', severity: 'error', summary: res.message , detail: 'Failed' })
            this.displayForm = true
          } else {
            this.loadDictionaries(this.lastTableLazyLoadEvent)
            this.messageService.add({ key: 'Message', severity: 'success', summary:"Success Add New Dictionaries" , detail: 'Successful' })
            this.displayForm = false
          }
        },(err) => {
          // console.log(err)
          this.displayForm = true
          if(err.name == "HttpErrorResponse") {
            this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Edit Dictionary" , detail: 'Code Already Exists' })
            }
            else {
              this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Add New Dictionaries" , detail: 'Failed' })
            }
        })
      }
    }
  }


}
