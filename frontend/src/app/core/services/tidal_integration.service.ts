import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {IntegrationService} from "@services/integration.service";
import {
    calculatePKCECodeChallenge,
    generateRandomCodeVerifier,
    generateRandomState,
} from "oauth4webapi";

@Injectable({
    providedIn: 'root'
})
export class TidalIntegrationService implements IntegrationService {

    private readonly clientId = environment.tidalClientId;
    private readonly redirectUri = environment.tidalRedirectUrl;
    private readonly authorizationEndpoint = 'https://login.tidal.com/authorize';
    private readonly code_challenge_method = 'S256';
    private STATE_KEY = 'tidal_state';
    private CODE_VERIFIER_KEY = 'tidal_code_verifier';

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
            this.CODE_VERIFIER_KEY,
            verifier
        );
        sessionStorage.setItem(
            this.STATE_KEY,
            state
        )

        // redirect user to Tidal's authorization page
        window.location.href = authorizationUrl.toString();
    }

    // Called when app redirects back from Tidal
    async finaliseAuth() {
        // TODO: make a call to my own backend to exchange the code for an refresh token
    }

    private getCodeVerifier(): string {
        const verifier = sessionStorage.getItem(this.CODE_VERIFIER_KEY);

        if (!verifier) {
            throw new Error('Missing PKCE code verifier');
        }

        return verifier;
    }

    private getState(): string {
        const state = sessionStorage.getItem(this.STATE_KEY);

        if (!state) {
            throw new Error('Missing OAuth state');
        }

        return state;
    }
}