import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component'
import { GigFormComponent } from './gig-form/gig-form.component'
import {LoginComponent} from "./login/login.component";
import {SignupComponent} from "./signup/signup.component";

const routeConfig: Routes = [
  {
    path: 'add-gig',
    component: GigFormComponent,
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'signup',
    component: SignupComponent
  },
  {
    path: '',
    component: HomeComponent,
  },
];

export default routeConfig;
