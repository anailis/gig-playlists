import {OAuthConfig} from "@models/oauthconfig";
import {environment} from "@environments/environment";

export const spotifyAuthConfig: OAuthConfig = {
    appName: "SPOTIFY",
    clientId: environment.spotifyClientId,
    redirectUrl: environment.spotifyRedirectUrl,
    authorizationUrl: "https://accounts.spotify.com/authorize",
    tokenUrl: "https://accounts.spotify.com/api/token",
    scope: "playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative"
};

export const tidalAuthConfig: OAuthConfig = {
    appName: "TIDAL",
    clientId: environment.tidalClientId,
    redirectUrl: environment.tidalRedirectUrl,
    authorizationUrl: "https://login.tidal.com/authorize",
    tokenUrl: "https://auth.tidal.com/v1/oauth2/token",
    scope: "playlists.write"
};