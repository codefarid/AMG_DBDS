import { Component } from '@angular/core';
import { LayoutService } from "./service/app.layout.service";

@Component({
    selector: 'app-footer',
    templateUrl: './app.footer.component.html'
})
export class AppFooterComponent {
    
    currentYear: any

    constructor(public layoutService: LayoutService) {
        this.currentYear = new Date().getFullYear();
    }
}
