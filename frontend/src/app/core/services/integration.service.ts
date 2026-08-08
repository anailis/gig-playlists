import {ActivatedRoute} from "@angular/router";
import {HttpClient} from "@angular/common/http";
import {inject} from "@angular/core";

export abstract class IntegrationService {

    protected route = inject(ActivatedRoute);
    protected httpClient = inject(HttpClient);
    protected STATE_KEY = "state";

    abstract integrate(): void;

    abstract exchangeCode(code: string | null): any;

    verifyState(returnedState: string | null): boolean {
        const storedState = sessionStorage.getItem(this.STATE_KEY);

        if (!returnedState || !storedState) {
            return false;
        }

        return returnedState === storedState;
    }

    // Called when app redirects back from the integration service
    async finaliseAuth() {
        this.route.queryParamMap.subscribe(params => {
            const code = params.get('code');
            const state = params.get('state');

            if (!this.verifyState(state)) {
                console.error('OAuth state mismatch');
                return;
            }

            this.exchangeCode(code).subscribe();
        });
    }
}