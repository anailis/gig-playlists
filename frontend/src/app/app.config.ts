import { ApplicationConfig } from '@angular/core';
import {provideHttpClient, withInterceptors} from '@angular/common/http';
import { provideRouter } from '@angular/router';
import routeConfig from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {authInterceptor} from "@core/interceptors/auth.interceptor";

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
        withInterceptors([authInterceptor])
    ),
    provideRouter(routeConfig),
    provideAnimationsAsync()
  ]
};
