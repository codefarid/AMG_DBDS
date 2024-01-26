import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { LazyLoadEvent, MessageService, ConfirmationService, ConfirmEventType, MenuItem } from 'primeng/api';
import { MasterService } from 'src/app/service/master.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.scss']
})
export class CategoryComponent implements OnInit {
  value = ''
  modalTitle = ''
  displayForm = false
  isEdit = false
  loading = false
  getId = ''
  
  categories : any[] = []
  stateOptions: any[] = [
    { label: 'Off', value: 'inactive' },
    { label: 'On', value: 'active' }
    ];

  inputForm!: FormGroup;
  constructor(
    private fb: FormBuilder, 
    private api: MasterService,
    private confirmationService: ConfirmationService,
    private messageService: MessageService,
    private router: Router) {
    
  }
  ngOnInit(): void {
   this.createForm()
   this.loadCategories()
  }

  formatDate(val:any) {
    if(val !== "None") {
      const year = val.slice(0, 4);
      const month = val.slice(4, 6);
      const day = val.slice(6, 8);
      const formattedDate = `${day}-${month}-${year}`;
      return formattedDate;
    } else {
      return val;
    }
  }

  togleStatusEdit(val:any) {
    if(val == "None"){
      let y = 'inactive'
      return y
    } else {
      const x = this.stateOptions.find(({ value }) => value === val);
      return x.value
    }
  }

  loadCategories(){
    this.loading = true
    setTimeout(() => {
      this.api.getCategories().subscribe((data) => {
        this.categories = data.result.map((el:any) => {
          return {
            code: el.code,
            label: el.label,
            created: this.formatDate(el.created),
            user: el.user
          }
        })
        // console.log(data)
        this.loading = false
      },(err) => {
        this.loading = false
        // console.log(err)
      })
    }, 1000);
  }

  createForm(){
    this.inputForm = this.fb.group({
      ctText: [''],
      stCate: ['active']
    });
  }

  goToTemp() {
    // console.log("clikced")
    this.router.navigate(['/master/temp'])
  }

  submitForm(){
    const userInput = this.inputForm.getRawValue()
    // console.log(userInput, this.getId)
    if (this.inputForm.invalid) {
      this.messageService.add({ key: 'Message', severity: 'error', summary: 'Submit Form', detail: 'Failed, there is empty data' })
    } else {
      if(this.isEdit) {
        this.api.putCategories(userInput, this.getId).subscribe((res) => {
          // console.log(res)
          if(res.message == 'Nama Sudah Ada, Buat Nama lain!') {
            this.displayForm = true
            this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Add New Categories" , detail: res.message })
          } else {
          this.displayForm = false
          this.loadCategories()
          this.messageService.add({ key: 'Message', severity: 'success', summary: "Success Edit Categories" , detail: 'Successful' })
          }
        }, (err) => {
          this.displayForm = true
          this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Edit Categories" , detail: 'Failed' })
          // console.log(err)
        })
      } else {
        this.api.postCategories(userInput).subscribe((res) => {
          // console.log(res)
          if(res.message == 'Nama Sudah Ada, Buat Nama lain!') {
            this.displayForm = true
            this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Add New Categories" , detail: res.message })
          } else {
            this.messageService.add({ key: 'Message', severity: 'success', summary:"Success Add New Categories" , detail: 'Successful' })
            this.displayForm = false
            this.loadCategories()
          }          
        },(err) => {
          this.displayForm = true
          this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Add New Categories" , detail: err.message })
        })
      }
    }
    
  }
  showForm() {
    this.isEdit = false;
    this.modalTitle = 'Create a Categories';
    this.inputForm.controls['ctText'].enable()
    this.inputForm.reset()
    this.displayForm = true;
  }
  showEditForm(data:any) {
    this.isEdit = true;
    this.modalTitle = 'Edit Categories';
    this.displayForm = true;
    this.getId = data.code
    console.log(this.getId,'///')
    this.api.getOneCategory(this.getId).subscribe((res) => {
      let cat = res.result[0]
      console.log(res)
      this.inputForm.patchValue({
        ctText: cat.label,
        stCate: this.togleStatusEdit(cat.status)
      })
    }, (err) => {
      // console.log(err)
      this.messageService.add({ key: 'Message', severity: 'error', summary: "Failed Get One Category" , detail: err.message })
    })
    
  }
}
