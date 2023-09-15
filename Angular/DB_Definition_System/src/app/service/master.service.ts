import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GlobalConstants } from './global';

@Injectable({
  providedIn: 'root'
})
export class MasterService {
  baseURL = GlobalConstants.baseURL + 'api'

  httpHeaders : any = new HttpHeaders({
    'Content-Type' : 'application/json',
    'Authorization': localStorage.getItem('token') ?? '',
    'App' : GlobalConstants.app
  })
  
  uploadHeaders : any = new HttpHeaders({
    'Authorization': localStorage.getItem('token') ?? '',
    'App' : GlobalConstants.app
  })

  constructor(
    private http:HttpClient,
  ) { }
  
  getMaterialInput(): Observable<any> {
    return this.http.get(this.baseURL+'/query_generator', {headers: this.httpHeaders})
  }

  postPreviewQuery(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/query_generator', data,{headers: this.httpHeaders})
  }

  postPreviewExtQuery(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/query_generator_ext', data,{headers: this.httpHeaders})
  }

  editPreviewQuery(data:any,id:any): Observable<any> {
    return this.http.put(this.baseURL+'/query_generator/'+id , data ,{headers: this.httpHeaders})
  }

  getOneTable(id:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_dbds/'+id, {headers: this.httpHeaders})
  }

  getAllTable(parameter:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_dbds', {headers: this.httpHeaders, params: parameter})
  }

  postCreateTable(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/master_dbds', data, {headers: this.httpHeaders})
  }

  putSelectedTable(data: any, id: any): Observable<any> {
    return this.http.put(this.baseURL+'/master_dbds/'+id, data, {headers: this.httpHeaders})
  }

  putSelectedExtTable(data:any, id:any): Observable<any> {
    return this.http.put(this.baseURL+'/master_dbds_ext/'+id, data, {headers: this.httpHeaders})
  }
  
  getTableAndFields(): Observable<any> {
    return this.http.get(this.baseURL+'/master_definition', {headers: this.httpHeaders})
  }
  
  getDetailedFields(id:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_definition/'+ id, {headers: this.httpHeaders})
  }

  updateStatusTable(id:any): Observable<any> {
    return this.http.delete(this.baseURL+'/master_dbds/'+id,{headers: this.httpHeaders})
  }

  postExtTable(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/master_dbds_ext',data, {headers: this.httpHeaders})
  }

  getCategories(): Observable<any> {
    return this.http.get(this.baseURL+'/master_categories', {headers: this.httpHeaders})
  }

  postCategories(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/master_categories', data, {headers:this.httpHeaders})
  }

  getOneCategory(id:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_categories/'+id, {headers: this.httpHeaders})
  }
  
  putCategories(data:any, id:any):Observable<any> {
    return this.http.put(this.baseURL+'/master_categories/'+id, data, {headers: this.httpHeaders})
  }

  getDictionaries(parameter:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_dictionaries', {headers: this.httpHeaders, params: parameter})
  }
  
  postDictionaries(data:any): Observable<any> {
    return this.http.post(this.baseURL+'/master_dictionaries', data, {headers: this.httpHeaders})
  }
  
  getOneDictionaries(id:any): Observable<any> {
    return this.http.get(this.baseURL+'/master_dictionaries/'+id,{headers: this.httpHeaders})
  }

  putDictionaries(data:any, id:any): Observable<any> {
    return this.http.put(this.baseURL+'/master_dictionaries/'+id, data, {headers: this.httpHeaders})
  }

  getDataFkey(): Observable<any> {
    return this.http.get(this.baseURL+'/query_generator/getFkeyData', {headers:this.httpHeaders})
  }

  downloadQuerries(data:any): Observable<any> {
    return this.http.post(`${this.baseURL}/master_dbds/post/downloads`,data,{headers: this.httpHeaders})
  }

  getDownloadQuerries(fileName:any): Observable<any> {
    return this.http.get(`${this.baseURL}/master_dbds/downloads/${fileName}`,{headers: this.httpHeaders})
  }

  deleteAfterDownloads(fileName:any): Observable<any> {
    return this.http.get(`${this.baseURL}/master_dbds/delete/downloads/${fileName}`,{headers:this.httpHeaders})
  }

  getFilteringApp(appName:any):Observable<any> {
    return this.http.get(`${this.baseURL}/master_dbds/${appName}`,{headers:this.httpHeaders})
  }
}
