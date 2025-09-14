import {Component, computed, EventEmitter, inject, Output, signal} from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIconButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {AuthbarComponent} from "../authbar/authbar.component";
import {NavService} from "@services/nav.service";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    MatToolbar,
    MatIconButton,
    MatIcon,
    AuthbarComponent
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  private navService = inject(NavService);
  @Output() navBarCollapsed = new EventEmitter<boolean>();

  menuClick() {
    this.navService.toggleNavbar();
    this.navBarCollapsed.emit(this.navService.getNavBarStatus());
  }

}
