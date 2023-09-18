import { Component, ElementRef, ViewChild } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../service/auth.service';
import { LayoutService } from "./service/app.layout.service";
import { JwtHelperService } from '@auth0/angular-jwt';

@Component({
    selector: 'app-topbar',
    templateUrl: './app.topbar.component.html'
})
export class AppTopBarComponent {

    jwtHelper = new JwtHelperService()
    appName = 'DB Definition System'
    items!: MenuItem[];
    user: any
    

    @ViewChild('menubutton') menuButton!: ElementRef;

    @ViewChild('topbarmenubutton') topbarMenuButton!: ElementRef;

    @ViewChild('topbarmenu') menu!: ElementRef;


    constructor(
        public layoutService: LayoutService,
        private authService: AuthService
    ){
        // this.user = authService.user
        const token = this.getToken()
        const decode = this.jwtHelper.decodeToken(token)
        this.user = decode.name
        // this.user = "Santoso"
    }

    getToken(): string {
        return localStorage.getItem('token') || '';
     }

    logout(){
        this.authService.logout();
    }
}
