import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { Amplify } from "aws-amplify";
import {environment} from "./app/config";

Amplify.configure({
    Auth: {
        Cognito: {
            userPoolClientId: '205m3ah5f7m3gf17hadbo7c16n',
            userPoolId: 'eu-west-2_ipRVC2a/s0',
            loginWith: {
                oauth: {
                    domain: environment.authUrl,
                    scopes: ['openid'],
                    responseType: 'code',
                    redirectSignIn: ['http://localhost:4201'],
                    redirectSignOut: ['http://localhost:4201']
                }
            },
        }
    }
});

bootstrapApplication(AppComponent, appConfig).catch((err) => console.error(err));
