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
    private loggedOutNavBarItems: NavItem[] = [
        { icon: 'music_note', label: 'About', route: 'home'},
    ];

    private loggedInNavBarItems: NavItem[] = [
        { icon: 'calendar_month', label: 'Gigs', route: 'gigs'},
        { icon: 'music_note', label: 'Playlists', route: 'playlists'},
        { icon: 'person', label: 'Account', route: 'account'},
    ];

    constructor() {}

    getNavBarItems(isLoggedIn: boolean): NavItem[] {
        return isLoggedIn ? this.loggedInNavBarItems : this.loggedOutNavBarItems;
    }
}