import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component'
import { GigFormComponent } from './gig-form/gig-form.component'

const routeConfig: Routes = [
  {
    path: 'add-gig',
    component: GigFormComponent,
  },
  {
    path: '',
    component: HomeComponent,
  },
];

export default routeConfig;
