import {Component, computed, signal} from '@angular/core';
import { RouterModule } from '@angular/router';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatSidenavModule} from "@angular/material/sidenav";
import {NavbarComponent} from "./shared/layout/navbar/navbar.component";
import {AuthbarComponent} from "./shared/layout/authbar/authbar.component";

@Component({
  standalone: true,
  selector: 'app-component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
    imports: [
        RouterModule,
        MatToolbarModule,
        MatButtonModule,
        MatIconModule,
        MatSidenavModule,
        NavbarComponent,
        AuthbarComponent
    ]
})
export class AppComponent {

  navbarCollapsed = signal(false)

  navbarWidth= computed(() => this.navbarCollapsed() ? '115px' : '250px');
}
