import {AuthService} from "@services/auth.service";
import {from, switchMap} from "rxjs";
import {HttpInterceptorFn} from "@angular/common/http";
import {inject} from "@angular/core";


export const authInterceptor: HttpInterceptorFn = (req, next) => {
    const authService = inject(AuthService);

    return from(authService.getToken()).pipe(
        switchMap(token => {
            const authReq = req.clone({
                setHeaders: { Authorization: token },
            });
            return next(authReq);
        })
    );
};