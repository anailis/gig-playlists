import {Injectable} from "@angular/core";
import {IntegrationService} from "@services/integration.service";

@Injectable({
    providedIn: 'root'
})
export class SpotifyIntegrationService implements IntegrationService {

    integrate(): void {
        console.log("Not implemented yet :(")
    }

}