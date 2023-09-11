import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { MessageService } from 'primeng/api';
import { GlobalConstants } from './global';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  baseUrl = GlobalConstants.baseURL
  httpHeaders : any = new HttpHeaders({
    'Content-Type': 'application/json',
    'Authorization': localStorage.getItem('token') as string,
    'App': GlobalConstants.app
  });
  
  jwtHelper = new JwtHelperService()
  programId: any
  auth: any
  user: any
  
  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private router: Router
  ) {}

  isLoggedIn(){
    const token = localStorage.getItem('token');    
    if (token) {
      this.user = this.jwtHelper.decodeToken(token)['name']
      return !this.jwtHelper.isTokenExpired(token);
    }
    return false;
  }

  getMenu(){
    return this.http.get(this.baseUrl + 'api/master_menu', {headers: this.httpHeaders})
  }

  logout(){
    localStorage.removeItem('token')
    this.router.navigate(['/'])
    window.location.reload()
  }

  isAuthorized(programId: any){
    return this.http.get(this.baseUrl + 'api/master_menu/auth/' + programId, {headers: this.httpHeaders})
  }

  validateFormEntry(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(field => {
      const control = formGroup.get(field);
      if (control instanceof FormControl) {
        control.markAsTouched({ onlySelf: true })
      }
    })
  }

  notAuthorized(errorCode: any, msg = ''){
    if(errorCode == 403){
      this.messageService.add({key: 'Message', severity:'error', summary: 'Error', detail: 'Token Not Authorized'});
      setTimeout(()=>{    
        localStorage.clear()            
        this.router.navigate(['/'])
      }, 2000)
    }else{
      if(errorCode == 401){
        this.messageService.add({key: 'Message', severity:'error', summary: 'Error', detail: 'User Not Authorized'});
      }else{
        if(errorCode == 500){
          this.messageService.add({key: 'Message', severity:'error', summary: 'Error', detail: msg});
        }else{
          this.messageService.add({key: 'Message', severity:'error', summary: 'Error', detail: 'Internal Server Error'});
        }        
      }
    }
  }
}
