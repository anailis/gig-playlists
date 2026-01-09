import {Injectable} from "@angular/core";
import { getCurrentUser, signOut, signInWithRedirect, AuthUser, fetchAuthSession } from 'aws-amplify/auth';
import {BehaviorSubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    private signedIn = new BehaviorSubject<boolean>(false);
    public isSignedIn$ = this.signedIn.asObservable();
    public user: AuthUser | null = null;

    constructor() {
        this.checkUser();
    }

    private checkUser() {
        try {
            getCurrentUser().then((user: AuthUser) => {
                this.user = user;
                this.signedIn.next(true);
            });
        } catch(err) {
            console.log("Not logged in");
            console.log(err);
            this.signedIn.next(false)
        }
    }

    async signOut(): Promise<void> {
        await signOut({
            global: true
        });
    }

    async signIn(): Promise<void> {
        await signInWithRedirect();
    }

    getUserId(): string | null {
        if (this.user) {
            return this.user.userId;
        }
        return null;
    }

    async getToken(): Promise<string> {
        const session = await fetchAuthSession({ forceRefresh: true });
        const accessToken = session.tokens?.accessToken.toString();
        if (accessToken) {
            return accessToken;
        } else {
            throw new Error("No auth token available");
        }
    }
}