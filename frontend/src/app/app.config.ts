import { ApplicationConfig } from '@angular/core';
import {provideHttpClient, withInterceptors, withXhr} from '@angular/common/http';
import { provideRouter } from '@angular/router';
import routeConfig from './app.routes';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {authInterceptor} from "@core/interceptors/auth.interceptor";

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withXhr(), 
        withInterceptors([authInterceptor])
    ),
    provideRouter(routeConfig),
    provideAnimationsAsync()
  ]
};
