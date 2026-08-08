import {Injectable} from "@angular/core";
import {IntegrationService} from "@services/integration.service";
import {generateRandomState} from "oauth4webapi";
import {environment} from "@environments/environment";

@Injectable({
    providedIn: 'root'
})
export class SpotifyIntegrationService extends IntegrationService {

    private readonly clientId = environment.spotifyClientId;
    private readonly redirectUri = environment.spotifyRedirectUrl;
    private readonly authorizationEndpoint = 'https://accounts.spotify.com/authorize';
    private readonly tokenEndpoint = 'https://accounts.spotify.com/api/token';
    private readonly scope = 'playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative';

    integrate(): void {
        const state = generateRandomState();

        const authorizationUrl = new URL(this.authorizationEndpoint);
        authorizationUrl.searchParams.set('client_id', this.clientId);
        authorizationUrl.searchParams.set('redirect_uri', this.redirectUri);
        authorizationUrl.searchParams.set('response_type', 'code');
        authorizationUrl.searchParams.set('scope', this.scope);
        authorizationUrl.searchParams.set('state', state);

        sessionStorage.setItem(
            this.STATE_KEY,
            state
        )

        // redirect user to Spotify's authorization page
        window.location.href = authorizationUrl.toString();
    }

    exchangeCode(code: string | null) {
        const payload = {
            "refresh_token_uri": this.tokenEndpoint,
            "client_id": this.clientId,
            "redirect_uri": this.redirectUri,
            "code": code,
            "code_verifier": "dummy",
            "type": "SPOTIFY",
            "scope": this.scope
        };

        return this.httpClient.post(
            environment.tokenExchangeUrl,
            payload
        );
    }

}