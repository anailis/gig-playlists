import {Injectable} from "@angular/core";
import {environment} from "../../config";


export interface AuthItem {
    icon: string;
    label: string;
    link: string;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private loggedOutAuthBarItems: AuthItem[] = [
        { icon: 'login', label: 'Login', link: environment.loginUrl },
        { icon: 'add', label: 'Signup', link: environment.signupUrl },
    ];

    private loggedInAuthBarItems: AuthItem[] = [
        { icon: 'logout', label: 'Logout', link: environment.logoutUrl },
    ];

    constructor() {}

    getAuthBarItems(isLoggedIn: boolean): AuthItem[] {
        return isLoggedIn ? this.loggedInAuthBarItems : this.loggedOutAuthBarItems;
    }
}