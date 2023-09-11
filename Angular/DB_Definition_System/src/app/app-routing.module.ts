import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { AppLayoutComponent } from "./layout/app.layout.component";
import { AuthGuard } from './Guard/auth.guard';
import { DBDSComponent} from './Master/dbds/dbds.component';
import { AddDefComponent } from './Master/add-def/add-def.component';
import { CategoryComponent } from './Master/category/category.component';
import { DictionaryComponent } from './Master/dictionary/dictionary.component';


const routes: Routes = [
    {
        path: '', 
        // data: { programId: '00000' },
        component: AppLayoutComponent,
        canActivate:[],
        title: "DBDS",
        children: [
            {
                path: 'master', 
                data: { programId: '1' },
                // canActivate:[AuthGuard],
                title: 'Master',
                children: [
                    {
                    path: 'sdb', 
                    data: { programId: '1' },
                    component: DBDSComponent,
                    title: "Setup Database",
                    canActivate:[],
                    children: []
                },{
                    path: 'edb', 
                    data: { programId: '2' },
                    component: AddDefComponent,
                    title: "Setup Database",
                    canActivate:[],
                    children: []
                },{
                    path: 'categories', 
                    data: { programId: '3' },
                    component: CategoryComponent,
                    title: "categories",
                    canActivate:[],
                    children: []
                },{
                    path: 'dictionaries', 
                    data: { programId: '4' },
                    component: DictionaryComponent,
                    title: "dictionaries",
                    canActivate:[],
                    children: []
                }
                ]
            }
        ]
    }
]

@NgModule({
    imports: [
        RouterModule.forRoot(routes)
    ],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
