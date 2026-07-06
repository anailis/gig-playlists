import { Component, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import {MatListItem, MatListItemIcon, MatListItemTitle, MatNavList} from "@angular/material/list";
import {MatIcon} from "@angular/material/icon";

import {environment} from "@environments/environment";
import {AuthService} from "@services/auth.service";

export interface AuthItem {
    icon: string;
    label: string;
    link: string;
}

@Component({
    selector: 'app-authbar',
    imports: [
    MatNavList,
    MatIcon,
    MatListItemIcon,
    MatListItemTitle,
    MatListItem
],
    templateUrl: './authbar.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './authbar.component.css'
})
export class AuthbarComponent implements OnInit {
    private authService = inject(AuthService);


    protected readonly environment = environment;
    isLoggedIn = false;

    loggedOutAuthItems: AuthItem[] = [
        { icon: 'add', label: 'Signup', link: environment.signupUrl },
    ];

    ngOnInit() {
        this.authService.isSignedIn$.subscribe(isSignedIn => {
            this.isLoggedIn = isSignedIn;
        });
    }

    async signOut(): Promise<void> {
        await this.authService.signOut();
    }

    async signIn(): Promise<void> {
        await this.authService.signIn();
    }

}
