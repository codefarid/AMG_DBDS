import { Component, ElementRef, ViewChild } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../service/auth.service';
import { LayoutService } from "./service/app.layout.service";

@Component({
    selector: 'app-topbar',
    templateUrl: './app.topbar.component.html'
})
export class AppTopBarComponent {

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
        // console.log(authService)
        this.user = "Santoso"
    }

    logout(){
        this.authService.logout();
    }
}
