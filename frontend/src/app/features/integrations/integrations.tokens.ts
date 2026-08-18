import {IntegrationService} from "@services/integration.service";
import {InjectionToken} from "@angular/core";
import {OAuthConfig} from "@models/oauthconfig";


export const SPOTIFY_OAUTH_CONFIG =
    new InjectionToken<OAuthConfig>('SPOTIFY_OAUTH_CONFIG');

export const TIDAL_OAUTH_CONFIG =
    new InjectionToken<OAuthConfig>('TIDAL_OAUTH_CONFIG');

export const INTEGRATION_SERVICES =
    new InjectionToken<IntegrationService>('INTEGRATION_SERVICES');