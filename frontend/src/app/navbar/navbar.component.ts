import {Component, signal} from '@angular/core';
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";

export type SidenavMenuItem = {
  icon: string;
  label: string;
  route: string;
}

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    NgOptimizedImage,
    MatListModule,
    MatIconModule
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  menuItems = signal<SidenavMenuItem[]>([
    {
      icon: 'calendar_month',
      label: 'Gigs',
      route: 'gigs',
    },
    {
      icon: 'music_note',
      label: 'Playlists',
      route: 'playlists',
    },
    {
      icon: 'person',
      label: 'Account',
      route: 'account',
    },
  ]);

}
