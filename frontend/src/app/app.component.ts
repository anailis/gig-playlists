import {Component, computed, signal} from '@angular/core';
import { RouterModule } from '@angular/router';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatSidenavModule} from "@angular/material/sidenav";
import {NavbarComponent} from "./shared/layout/navbar/navbar.component";
import {AuthbarComponent} from "./shared/layout/authbar/authbar.component";
import {HeaderComponent} from "./shared/layout/header/header.component";

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
        HeaderComponent
    ]
})
export class AppComponent {
    // TODO: fix this to use the values from HeaderComponent
    navbarCollapsed = signal(true);
    navbarWidth= computed(() => this.navbarCollapsed() ? '65px' : '200px');
}