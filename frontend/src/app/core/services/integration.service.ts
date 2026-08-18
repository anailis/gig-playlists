import {ActivatedRoute} from "@angular/router";
import {HttpClient} from "@angular/common/http";
import {inject} from "@angular/core";
import {environment} from "@environments/environment";
import {OAuthConfig} from "@models/oauthconfig";
import {calculatePKCECodeChallenge, generateRandomCodeVerifier, generateRandomState} from "oauth4webapi";
import {IntegrationType} from "@models/user";

export class IntegrationService {

    protected route = inject(ActivatedRoute);
    protected httpClient = inject(HttpClient);
    private readonly codeChallengeMethod = 'S256';
    private readonly state_key: string;
    private readonly code_verifier_key: string;
    private appName: IntegrationType;

    constructor(
        private readonly config: OAuthConfig
    ) {
        this.config = config;
        this.appName = config.appName;
        this.state_key = `${config.appName}_state`;
        this.code_verifier_key = `${config.appName}_code_verifier`;
    }

    getAppName(): IntegrationType {
        return this.appName;
    }

    async integrate() {
        const verifier = generateRandomCodeVerifier();
        const challenge = await calculatePKCECodeChallenge(verifier);
        const state = generateRandomState();

        const authorizationUrl = new URL(this.config.authorizationUrl);
        authorizationUrl.searchParams.set('client_id', this.config.clientId);
        authorizationUrl.searchParams.set('redirect_uri', this.config.redirectUrl);
        authorizationUrl.searchParams.set('response_type', 'code');
        authorizationUrl.searchParams.set('scope', this.config.scope);
        authorizationUrl.searchParams.set('code_challenge', challenge);
        authorizationUrl.searchParams.set('code_challenge_method', this.codeChallengeMethod);
        authorizationUrl.searchParams.set('state', state);

        sessionStorage.setItem(
            this.code_verifier_key,
            verifier
        );
        sessionStorage.setItem(
            this.state_key,
            state
        )

        // redirect user to third party authorization page
        window.location.href = authorizationUrl.toString();
    }

    // Called when app redirects back from the integration service
    async finaliseAuth() {
        this.route.queryParamMap.subscribe(params => {
            const code = params.get('code');
            const state = params.get('state');

            if (!this.verifyState(state)) {
                console.error('OAuth state mismatch');
                return;
            }

            this.exchangeCode(code).subscribe();
        });
    }

    private verifyState(returnedState: string | null): boolean {
        const storedState = sessionStorage.getItem(this.state_key);

        if (!returnedState || !storedState) {
            return false;
        }

        return returnedState === storedState;
    }

    private getCodeVerifier(): string {
        const verifier = sessionStorage.getItem(this.code_verifier_key);

        if (!verifier) {
            throw new Error('Missing PKCE code verifier');
        }

        return verifier;
    }

    private exchangeCode(code: string | null) {
        const verifier = this.getCodeVerifier();
        const payload = {
            "refresh_token_uri": this.config.tokenUrl,
            "client_id": this.config.clientId,
            "redirect_uri": this.config.redirectUrl,
            "code": code,
            "code_verifier": verifier,
            "type": "TIDAL",
            "scope": this.config.scope
        };

        return this.httpClient.post(
            environment.tokenExchangeUrl,
            payload
        );
    }
}