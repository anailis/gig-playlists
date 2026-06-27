import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {IntegrationService} from "@services/integration.service";
import {finalizeLogin, init as initAuth} from "@tidal-music/auth";
import {calculatePKCECodeChallenge, generateRandomCodeVerifier, generateRandomState} from "oauth4webapi";

@Injectable({
    providedIn: 'root'
})
export class TidalIntegrationService implements IntegrationService {

    private readonly clientId = environment.tidalClientId;
    private readonly redirectUri = environment.tidalRedirectUrl;
    private readonly authorizationEndpoint = 'https://login.tidal.com/authorize';
    private readonly code_challenge_method = 'S256'

    // Starts the OAuth login flow - redirects the browser away from the application.
    async integrate() {
        const verifier = generateRandomCodeVerifier();
        const challenge = await calculatePKCECodeChallenge(verifier);
        const state = generateRandomState();

        const authorizationUrl = new URL(this.authorizationEndpoint);
        authorizationUrl.searchParams.set('client_id', this.clientId);
        authorizationUrl.searchParams.set('redirect_uri', this.redirectUri);
        authorizationUrl.searchParams.set('response_type', 'code');
        // TODO: add scopes
        authorizationUrl.searchParams.set('scope', "");
        authorizationUrl.searchParams.set('code_challenge', challenge);
        authorizationUrl.searchParams.set('code_challenge_method', this.code_challenge_method);
        authorizationUrl.searchParams.set('state', state);

        sessionStorage.setItem(
            'tidal_code_verifier',
            verifier
        );

        window.location.href = authorizationUrl.toString();
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