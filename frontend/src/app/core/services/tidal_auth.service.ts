import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {credentialsProvider, finalizeLogin, init as initAuth, initializeLogin} from "@tidal-music/auth";

@Injectable({
    providedIn: 'root'
})
export class TidalAuthService {

    // retrieves an authorisation token
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

    // exchanges the authorisation token for an access token and refresh token
    async finaliseLogin() {
        const clientId = localStorage.getItem('clientId');
        const redirectUri = localStorage.getItem('redirectUri');

        if (clientId && redirectUri) {
            await initAuth({
                clientId,
                credentialsStorageKey: 'authorizationCode',
            });

            try {
                await finalizeLogin(window.location.search);
            } catch (err: any) {
                console.error('User already logged in or an error occurred:', err.message);
            }
        }
    }

    login() {
        localStorage.setItem('clientId', environment.tidalClientId);
        localStorage.setItem('redirectUri', environment.redirectUrl);

        this.authorize(environment.tidalClientId, environment.redirectUrl).catch(err => {});
    }
}