import {IntegrationType} from "@models/integration";

export interface OAuthConfig {
    appName: IntegrationType;
    clientId: string;
    authorizationUrl: string;
    tokenUrl: string;
    redirectUrl: string;
    scope: string;
}