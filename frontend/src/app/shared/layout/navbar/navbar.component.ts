import {Component, Input, signal, OnInit, inject, computed, Output, EventEmitter} from '@angular/core';
import {CommonModule} from "@angular/common";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {NavItem, NavService} from "@services/nav.service";
import {AuthService} from "@services/auth.service";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    MatListModule,
    MatIconModule,
    RouterLink,
    RouterLinkActive,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit {
  private navService = inject(NavService);
  private authService = inject(AuthService);

  isLoggedIn = false
  navItems: NavItem[] = [];
  navBarCollapsed = false;

  ngOnInit() {
    this.authService.isSignedIn$.subscribe(isSignedIn => {
      this.isLoggedIn = isSignedIn;
      this.updateNavItems();
    });

    this.navService.navBarCollapsed$.subscribe(collapsed => {
      this.navBarCollapsed = collapsed;
    })
  }

  private async updateNavItems() {
    this.navItems = this.navService.getNavBarItems(this.isLoggedIn);
  }

}
