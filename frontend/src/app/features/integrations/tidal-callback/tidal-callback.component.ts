import {Component, OnInit, ChangeDetectionStrategy, Inject} from '@angular/core';
import {Router} from "@angular/router";
import {TIDAL_INTEGRATION_SERVICE} from "@features/integrations/integrations.tokens";
import {IntegrationService} from "@services/integration.service";

@Component({
    selector: 'app-tidal-callback',
    imports: [],
    templateUrl: './tidal-callback.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './tidal-callback.component.css'
})
export class TidalCallbackComponent implements OnInit {
  constructor(
      @Inject(TIDAL_INTEGRATION_SERVICE)
      private readonly tidalIntegrationService: IntegrationService,

      private router: Router
  ) {}

  async ngOnInit() {

    await this.tidalIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
