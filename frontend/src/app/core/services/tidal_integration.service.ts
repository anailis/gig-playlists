import {Injectable} from "@angular/core";
import {environment} from "environments/environment";
import {IntegrationService} from "@services/integration.service";
import {init as initAuth, initializeLogin} from "@tidal-music/auth";

@Injectable({
    providedIn: 'root'
})
export class TidalIntegrationService implements IntegrationService {

    integrate() {
        localStorage.setItem('clientId', environment.tidalClientId);
        localStorage.setItem('redirectUri', environment.integrationRedirectUrl);

        this.authorise(environment.tidalClientId, environment.integrationRedirectUrl);
    }

    registerIntegration() {
        const params = Object.fromEntries(new URLSearchParams(window.location.search));

        if (params['code']) {
            console.log(params['code']);
        }
    }

    // retrieves an authorisation token
    async authorise(clientId: string, redirectUri: string) {
        await initAuth({
            clientId,
            credentialsStorageKey: 'authorizationCode',
        });

        const loginUrl = await initializeLogin({
            redirectUri,
        });

        window.open(loginUrl, '_self');
    }
}