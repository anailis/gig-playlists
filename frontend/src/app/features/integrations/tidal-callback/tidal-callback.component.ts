import {ChangeDetectionStrategy, Component, Inject, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {INTEGRATION_SERVICES} from "@features/integrations/integrations.tokens";
import {IntegrationService} from "@services/integration.service";
import {IntegrationType} from "@models/user";

@Component({
    selector: 'app-tidal-callback',
    imports: [],
    templateUrl: './tidal-callback.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './tidal-callback.component.css'
})
export class TidalCallbackComponent implements OnInit {
  private tidalIntegrationService: IntegrationService;

  constructor(
      @Inject(INTEGRATION_SERVICES)
      private readonly integrationServices: IntegrationService[],

      private router: Router
  ) {
      const tidalService = this.integrationServices.find(service => service.getAppName() === IntegrationType.TIDAL);

      if (!tidalService) {
          throw new Error(`No IntegrationService registered for TIDAL}`);
      }

      this.tidalIntegrationService = tidalService;
  }

  async ngOnInit() {

    await this.tidalIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
