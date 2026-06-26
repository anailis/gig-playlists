import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {IntegrationService} from "@services/integration.service";
import {credentialsProvider, finalizeLogin, init as initAuth, initializeLogin} from "@tidal-music/auth";

@Injectable({
    providedIn: 'root'
})
export class TidalIntegrationService implements IntegrationService {

    private readonly clientId = environment.tidalClientId;
    private readonly redirectUri = environment.tidalRedirectUrl;

    // Starts the OAuth login flow - redirects the browser away from the application.
    async integrate() {
        this.persistLoginContext()
        await this.authorise();
    }

    private persistLoginContext() {
        localStorage.setItem('clientId', this.clientId);
        localStorage.setItem('redirectUri', this.redirectUri);
    }

    async authorise() {
        await initAuth({
            clientId: this.clientId,
            credentialsStorageKey: 'authorizationCode',
        });

        const loginUrl = await initializeLogin({
            redirectUri: this.redirectUri,
        });

        // redirect
        window.location.href = loginUrl;
    }

    // Called when app redirects back from Tidal
    async finaliseAuth() {

        await initAuth({
            clientId: this.clientId,
            credentialsStorageKey: 'authorizationCode'
        });

        // pass query params from redirect
        await finalizeLogin(window.location.search);
    }
}