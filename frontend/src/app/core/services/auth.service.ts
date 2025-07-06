import {Injectable} from "@angular/core";
import {environment} from "../../config";
import { getCurrentUser } from 'aws-amplify/auth';


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

    async currentAuthenticatedUser() {
        try {
            const { username, userId, signInDetails } = await getCurrentUser();
            console.log(`The username: ${username}`);
            console.log(`The userId: ${userId}`);
            console.log(`The signInDetails: ${signInDetails}`);
        } catch (err) {
            console.log(err);
        }
    }

    async isSignedIn(): Promise<boolean> {
        try {
            await this.currentAuthenticatedUser();
            return true;
        } catch {
            return false;
        }
    }
}