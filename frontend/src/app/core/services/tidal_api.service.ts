import {Injectable} from "@angular/core";
import {createAPIClient} from "@tidal-music/api";
import {credentialsProvider} from "@tidal-music/auth";

@Injectable({
    providedIn: 'root'
})
export class TidalAPIService {

    private apiClient: any;

    async initApiClient() {
        await credentialsProvider.getCredentials();
        this.apiClient = createAPIClient(credentialsProvider);
    }

    async seeAlbum() {
        await this.initApiClient();

        await this.apiClient.GET('/playlists/ea3b9a0e-24f4-4408-ae39-d132952a32a0', {
            params: {
                query: { countryCode: 'US' },
            },
        });
    }
}