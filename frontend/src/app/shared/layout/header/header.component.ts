import {Component, computed, signal} from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIconButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatSidenavContainer} from "@angular/material/sidenav";
import {AuthbarComponent} from "../authbar/authbar.component";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbar,
    MatIconButton,
    MatIcon,
    MatSidenavContainer,
    AuthbarComponent
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  navbarCollapsed = signal(false)

  navbarWidth= computed(() => this.navbarCollapsed() ? '65px' : '200px');

}
