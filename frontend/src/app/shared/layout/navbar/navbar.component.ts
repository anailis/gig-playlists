import {Component, Input, signal} from '@angular/core';
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
export class NavbarComponent {

  isLoggedIn = false
  navItems: NavItem[] = [];

  constructor(
      private navService: NavService,
      private authService: AuthService
  ) {}

  navContentCollapsed = signal(false)
  @Input() set navbarCollapsed(val: boolean) {
    this.navContentCollapsed.set(val);
  }

  ngOnInit() {
    this.authService.isSignedIn$.subscribe(isSignedIn => {
      this.isLoggedIn = isSignedIn;
      this.updateNavItems();
    });
  }

  private async updateNavItems() {
    this.navItems = this.navService.getNavBarItems(this.isLoggedIn);
  }

}
