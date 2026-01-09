import { Routes } from '@angular/router';
import { GigFormComponent } from './features/gigs/gig-form/gig-form.component'
import {GigCalendar} from "./features/gigs/gig-calendar/gig-calendar.component";
import {AccountComponent} from "./features/account/account.component";
import {PlaylistsComponent} from "./features/playlists/playlists.component";
import {IntegrationsComponent} from "@features/integrations/integrations.component";

const routeConfig: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'home'
  },
  {
    path: 'gigs',
    component: GigCalendar,
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
    path: 'integrations',
    component: IntegrationsComponent,
  },
  {
    path: 'add-gig',
    component: GigFormComponent,
  },
];

export default routeConfig;
