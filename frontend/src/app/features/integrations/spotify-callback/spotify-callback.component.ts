import {Component, OnInit, ChangeDetectionStrategy, Inject} from '@angular/core';
import {Router} from "@angular/router";
import {SPOTIFY_INTEGRATION_SERVICE} from "@features/integrations/integrations.tokens";
import {IntegrationService} from "@services/integration.service";

@Component({
    selector: 'app-spotify-callback',
    imports: [],
    templateUrl: './spotify-callback.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './spotify-callback.component.css'
})
export class SpotifyCallbackComponent implements OnInit {
  constructor(
      @Inject(SPOTIFY_INTEGRATION_SERVICE)
      private readonly spotifyIntegrationService: IntegrationService,

      private router: Router
  ) {}

  async ngOnInit() {

    await this.spotifyIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
