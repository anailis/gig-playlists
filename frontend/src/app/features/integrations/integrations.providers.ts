import {OAuthConfig} from "@models/oauthconfig";
import {IntegrationService} from "@services/integration.service";
import {Provider} from "@angular/core";
import {
    INTEGRATION_SERVICES,
    SPOTIFY_OAUTH_CONFIG,
    TIDAL_OAUTH_CONFIG
} from "@features/integrations/integrations.tokens";
import {spotifyAuthConfig, tidalAuthConfig} from "@features/integrations/integrations.config";

export const OAUTH_PROVIDERS: Provider[] = [
    {
        provide: SPOTIFY_OAUTH_CONFIG,
        useValue: spotifyAuthConfig
    },
    {
        provide: TIDAL_OAUTH_CONFIG,
        useValue: tidalAuthConfig
    },
    {
        provide: INTEGRATION_SERVICES,
        useFactory: (config: OAuthConfig) => new IntegrationService(config),
        deps: [SPOTIFY_OAUTH_CONFIG],
        multi: true
    },
    {
        provide: INTEGRATION_SERVICES,
        useFactory: (config: OAuthConfig) => new IntegrationService(config),
        deps: [TIDAL_OAUTH_CONFIG],
        multi: true
    },
];