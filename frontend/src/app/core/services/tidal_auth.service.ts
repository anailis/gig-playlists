import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {init as initAuth, initializeLogin} from "@tidal-music/auth";

@Injectable({
    providedIn: 'root'
})
export class TidalAuthService {

    async authorize(clientId: string, redirectUri: string) {
        await initAuth({
            clientId,
            credentialsStorageKey: 'authorizationCode',
        });

        const loginUrl = await initializeLogin({
            redirectUri,
        });

        window.open(loginUrl, '_self');
    }

    login() {
        console.log("log me in!")
        this.authorize(environment.tidalClientId, environment.redirectUrl).catch(err => {})
    }
}