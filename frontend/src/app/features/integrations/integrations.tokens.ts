import {IntegrationService} from "@services/integration.service";
import {InjectionToken} from "@angular/core";
import {OAuthConfig} from "@models/oauthconfig";


export const SPOTIFY_OAUTH_CONFIG =
    new InjectionToken<OAuthConfig>('SPOTIFY_OAUTH_CONFIG');

export const TIDAL_OAUTH_CONFIG =
    new InjectionToken<OAuthConfig>('TIDAL_OAUTH_CONFIG');

export const SPOTIFY_INTEGRATION_SERVICE =
    new InjectionToken<IntegrationService>('SPOTIFY_INTEGRATION_SERVICE');

export const TIDAL_INTEGRATION_SERVICE =
    new InjectionToken<IntegrationService>('TIDAL_INTEGRATION_SERVICE');