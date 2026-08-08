import {OAuthConfig} from "@models/oauthconfig";
import {IntegrationService} from "@services/integration.service";
import {Provider} from "@angular/core";
import {
    SPOTIFY_INTEGRATION_SERVICE,
    SPOTIFY_OAUTH_CONFIG,
    TIDAL_INTEGRATION_SERVICE, TIDAL_OAUTH_CONFIG
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
        provide: SPOTIFY_INTEGRATION_SERVICE,
        useFactory: (config: OAuthConfig) => new IntegrationService(config),
        deps: [SPOTIFY_OAUTH_CONFIG],
    },
    {
        provide: TIDAL_INTEGRATION_SERVICE,
        useFactory: (config: OAuthConfig) => new IntegrationService(config),
        deps: [TIDAL_OAUTH_CONFIG],
    },
];