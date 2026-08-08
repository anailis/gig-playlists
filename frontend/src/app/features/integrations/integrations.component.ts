import {Component, inject, OnInit, ChangeDetectionStrategy, Inject} from '@angular/core';

import {MatCard, MatCardContent} from "@angular/material/card";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {IntegrationType} from "@models/user";
import {UserService} from "@services/user.service";
import {AuthService} from "@services/auth.service";
import {IntegrationService} from "@services/integration.service";
import {SPOTIFY_INTEGRATION_SERVICE, TIDAL_INTEGRATION_SERVICE} from "@features/integrations/integrations.tokens";

@Component({
    selector: 'app-playlists',
    imports: [
    MatCard,
    MatButton,
    MatIcon,
    MatCardContent
],
    templateUrl: './integrations.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './integrations.component.css'
})
export class IntegrationsComponent implements OnInit {

  userService: UserService = inject(UserService);
  authService: AuthService = inject(AuthService);

  userIntegrations: { name: IntegrationType; enabled: boolean }[] = [];
  userId: string | null = null;
    private readonly allowedIntegrations: Map<IntegrationType, IntegrationService>;

    constructor(
        @Inject(SPOTIFY_INTEGRATION_SERVICE)
        private readonly spotifyIntegrationService: IntegrationService,

        @Inject(TIDAL_INTEGRATION_SERVICE)
        private readonly tidalIntegrationService: IntegrationService
    ) {
        this.allowedIntegrations = new Map([
            [IntegrationType.SPOTIFY, spotifyIntegrationService],
            [IntegrationType.TIDAL, tidalIntegrationService],
        ])
    }

  ngOnInit() {
    this.userId = this.authService.getUserId();
    if (this.userId) {
      this.userService.getUser(this.userId).subscribe(user => {
        const userIntegrations = new Set(user.integrations);
        const integrations = Object.keys(this.allowedIntegrations) as IntegrationType[];
        this.userIntegrations = integrations.map(integration => ({
          name: integration,
          enabled: userIntegrations.has(integration),
        }));
      })
    }
  }

  statusOfAllowedIntegrations(): { name: IntegrationType; enabled: boolean }[] {
    return this.userIntegrations;
  }

  integrateWithThirdParty(integration: IntegrationType) {
     const integrationService = this.allowedIntegrations.get(integration);


      if (!integrationService) {
          throw new Error(`Unsupported integration: ${integration}`);
      }

     integrationService.integrate();
  }

}
