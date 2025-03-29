import { Routes } from '@angular/router';
import { GigFormComponent } from './gig-form/gig-form.component'

const routeConfig: Routes = [
  {
    path: 'add-gig',
    component: GigFormComponent,
  },
];

export default routeConfig;
