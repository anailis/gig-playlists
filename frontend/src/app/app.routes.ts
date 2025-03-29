import { Routes } from '@angular/router';
import { GigFormComponent } from './gig-form/gig-form.component'
import {GigsComponent} from "./pages/gigs/gigs.component";
import {AccountComponent} from "./pages/account/account.component";
import {PlaylistsComponent} from "./pages/playlists/playlists.component";

const routeConfig: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'home'
  },
  {
    path: 'gigs',
    component: GigsComponent,
  },
  {
    path: 'account',
    component: AccountComponent,
  },
  {
    path: 'playlists',
    component: PlaylistsComponent,
  },
  {
    path: 'add-gig',
    component: GigFormComponent,
  },
];

export default routeConfig;
