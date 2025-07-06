import {Component, Input, signal} from '@angular/core';
import {CommonModule} from "@angular/common";
import {MatListModule} from "@angular/material/list";
import {MatIconModule} from "@angular/material/icon";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {NavItem, NavService} from "@services/nav.service";

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

  constructor(private navService: NavService) {}

  navContentCollapsed = signal(false)
  @Input() set navbarCollapsed(val: boolean) {
    this.navContentCollapsed.set(val);
  }

  ngOnInit() {
    this.updateNavItems();
  }

  private updateNavItems() {
    this.navItems = this.navService.getNavBarItems(this.isLoggedIn);
  }

}
