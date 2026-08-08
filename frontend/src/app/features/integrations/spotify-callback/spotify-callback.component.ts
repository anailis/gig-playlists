import {Component, OnInit, ChangeDetectionStrategy} from '@angular/core';
import {Router} from "@angular/router";
import {SpotifyIntegrationService} from "@services/spotify_integration.service";

@Component({
    selector: 'app-spotify-callback',
    imports: [],
    templateUrl: './spotify-callback.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './spotify-callback.component.css'
})
export class SpotifyCallbackComponent implements OnInit {
  constructor(
      private spotifyIntegrationService: SpotifyIntegrationService,
      private router: Router
  ) {}

  async ngOnInit() {

    await this.spotifyIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
