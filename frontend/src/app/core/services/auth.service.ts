import {Injectable} from "@angular/core";
import { getCurrentUser, signOut, signInWithRedirect } from 'aws-amplify/auth';
import {BehaviorSubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    private signedIn = new BehaviorSubject<boolean>(false);
    public isSignedIn$ = this.signedIn.asObservable();

    constructor() {
        this.checkUser();
    }

    private async checkUser() {
        try {
            await getCurrentUser();
            this.signedIn.next(true)
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

}