import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { map, Observable } from 'rxjs';
import { AuthService } from '../service/auth.service';
import { GlobalConstants } from '../service/global';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService : AuthService,
    private router: Router
  ){}
  
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    
      if(this.authService.isLoggedIn()){
      var programId = route.data['programId']
      if(programId){
        if(programId == "00000"){
          return true
        }
        return this.authService.isAuthorized(programId).pipe(
          map((auth: any) => {
            if (auth) { 
              this.authService.programId = route.data['programId']
              this.authService.auth = auth
              if(auth[0] == 1){
                return true
              }else{
                this.router.navigate(['/']);
                return false
              }
            }
            this.router.navigate(['/']);
            return false;
          })
        )
      }
      this.router.navigate(['/']);
      return false;
    }else{
      window.location.href = GlobalConstants.loginPage
      return false
    }
  }
  
}
