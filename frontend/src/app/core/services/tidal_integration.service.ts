import {Injectable} from "@angular/core";
import {environment} from "@environments/environment";
import {IntegrationService} from "@services/integration.service";
import {
    calculatePKCECodeChallenge,
    generateRandomCodeVerifier,
    generateRandomState,
} from "oauth4webapi";

@Injectable({
    providedIn: 'root'
})
export class TidalIntegrationService extends IntegrationService {

    private readonly clientId = environment.tidalClientId;
    private readonly redirectUri = environment.tidalRedirectUrl;
    private readonly authorizationEndpoint = 'https://login.tidal.com/authorize';
    private readonly tokenEndpoint = 'https://auth.tidal.com/v1/oauth2/token';
    private readonly codeChallengeMethod = 'S256';
    private readonly SCOPE = 'playlists.write';
    private CODE_VERIFIER_KEY = 'tidal_code_verifier';


    async integrate() {
        const verifier = generateRandomCodeVerifier();
        const challenge = await calculatePKCECodeChallenge(verifier);
        const state = generateRandomState();

        const authorizationUrl = new URL(this.authorizationEndpoint);
        authorizationUrl.searchParams.set('client_id', this.clientId);
        authorizationUrl.searchParams.set('redirect_uri', this.redirectUri);
        authorizationUrl.searchParams.set('response_type', 'code');
        authorizationUrl.searchParams.set('scope', this.SCOPE);
        authorizationUrl.searchParams.set('code_challenge', challenge);
        authorizationUrl.searchParams.set('code_challenge_method', this.codeChallengeMethod);
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

    private getCodeVerifier(): string {
        const verifier = sessionStorage.getItem(this.CODE_VERIFIER_KEY);

        if (!verifier) {
            throw new Error('Missing PKCE code verifier');
        }

        return verifier;
    }

    exchangeCode(code: string | null) {
        const verifier = this.getCodeVerifier();
        const payload = {
            "refresh_token_uri": this.tokenEndpoint,
            "client_id": this.clientId,
            "redirect_uri": this.redirectUri,
            "code": code,
            "code_verifier": verifier,
            "type": "TIDAL",
            "scope": this.SCOPE
        };

        return this.httpClient.post(
            environment.tokenExchangeUrl,
            payload
        );
    }
}