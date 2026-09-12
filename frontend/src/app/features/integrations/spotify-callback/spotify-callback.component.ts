import {Component, OnInit, ChangeDetectionStrategy, Inject} from '@angular/core';
import {Router} from "@angular/router";
import {INTEGRATION_SERVICES} from "@features/integrations/integrations.tokens";
import {IntegrationService} from "@services/integration.service";
import {IntegrationType} from "@models/integration";

@Component({
    selector: 'app-spotify-callback',
    imports: [],
    templateUrl: './spotify-callback.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './spotify-callback.component.css'
})
export class SpotifyCallbackComponent implements OnInit {
  private spotifyIntegrationService: IntegrationService;

  constructor(
      @Inject(INTEGRATION_SERVICES)
      private readonly integrationServices: IntegrationService[],

      private router: Router
  ) {
      const spotifyService = this.integrationServices.find(service => service.getAppName() === IntegrationType.SPOTIFY);

      if (!spotifyService) {
          throw new Error(`No IntegrationService registered for SPOTIFY`);
      }

      this.spotifyIntegrationService = spotifyService;
  }

  async ngOnInit() {

    await this.spotifyIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
