import { Injectable } from '@angular/core';

export interface NavItem {
    icon: string;
    label: string;
    route: string;
}

@Injectable({
    providedIn: 'root'
})
export class NavService {
    private loggedOutNavItems: NavItem[] = [
        { icon: 'music_note', label: 'About', route: 'home'},
    ];

    private loggedInNavItems: NavItem[] = [
        { icon: 'calendar_month', label: 'Gigs', route: 'gigs'},
        { icon: 'music_note', label: 'Playlists', route: 'playlists'},
        { icon: 'person', label: 'Account', route: 'account'},
    ];

    constructor() {}

    getNavItems(isLoggedIn: boolean): NavItem[] {
        return isLoggedIn ? this.loggedInNavItems : this.loggedOutNavItems;
    }
}