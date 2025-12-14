import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { Amplify } from "aws-amplify";
import {environment} from "environments/environment";

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
                    redirectSignIn: [environment.redirectUrl],
                    redirectSignOut: [environment.redirectUrl]
                }
            },
        }
    }
});

bootstrapApplication(AppComponent, appConfig).catch((err) => console.error(err));
