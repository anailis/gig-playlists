import {Component, inject, OnInit, ChangeDetectionStrategy} from '@angular/core';

import {MatCard, MatCardContent} from "@angular/material/card";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {IntegrationType} from "@models/user";
import {UserService} from "@services/user.service";
import {AuthService} from "@services/auth.service";
import {IntegrationService} from "@services/integration.service";
import {TidalIntegrationService} from "@services/tidal_integration.service";
import {SpotifyIntegrationService} from "@services/spotify_integration.service";

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
  tidalIntegration: TidalIntegrationService = inject(TidalIntegrationService);
  spotifyIntegration: IntegrationService = inject(SpotifyIntegrationService);

  allowedIntegrations: Record<IntegrationType, IntegrationService> = {
    [IntegrationType.SPOTIFY]: this.spotifyIntegration,
    [IntegrationType.TIDAL]: this.tidalIntegration,
  }
  userIntegrations: { name: IntegrationType; enabled: boolean }[] = [];
  userId: string | null = null;

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
     const integrationService = this.allowedIntegrations[integration];
     integrationService.integrate();
  }

}
