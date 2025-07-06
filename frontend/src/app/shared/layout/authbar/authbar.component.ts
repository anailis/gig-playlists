import { Component } from '@angular/core';
import {MatListItem, MatListItemIcon, MatListItemTitle, MatNavList} from "@angular/material/list";
import {MatIcon} from "@angular/material/icon";
import {AuthItem, AuthService} from "@services/auth.service";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-authbar',
  standalone: true,
    imports: [
        MatNavList,
        MatIcon,
        MatListItemIcon,
        MatListItemTitle,
        MatListItem,
        NgForOf
    ],
  templateUrl: './authbar.component.html',
  styleUrl: './authbar.component.css'
})
export class AuthbarComponent {

    isLoggedIn = false;
    authItems: AuthItem[] = [];

    constructor(private authService: AuthService) {}

    ngOnInit() {
        this.updateAuthBar();
    }

    private updateAuthBar() {
        this.authItems = this.authService.getAuthBarItems(this.isLoggedIn);
    }


}
