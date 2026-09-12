import { provideZoneChangeDetection } from "@angular/core";
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { Amplify } from "aws-amplify";
import {environment} from "@environments/environment";
import {OAUTH_PROVIDERS} from "@features/integrations/integrations.providers";

Amplify.configure({
    Auth: {
        Cognito: {
            userPoolClientId: environment.userPoolClientId,
            userPoolId: environment.userPoolId,
            loginWith: {
                oauth: {
                    domain: environment.authUrl,
                    scopes: ['openid'],
                    responseType: 'code',
                    redirectSignIn: [environment.cognitoRedirectUrl],
                    redirectSignOut: [environment.cognitoRedirectUrl]
                }
            },
        }
    }
});

bootstrapApplication(
    AppComponent,
    {
        ...appConfig, providers: [
            provideZoneChangeDetection(),
            OAUTH_PROVIDERS,
            ...appConfig.providers
        ]
    }).catch((err) => console.error(err)
);
