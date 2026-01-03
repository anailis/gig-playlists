import {Component, inject} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
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
  standalone: true,
  imports: [
    NgForOf,
    MatCard,
    MatButton,
    MatIcon,
    MatCardContent,
    NgIf
  ],
  templateUrl: './integrations.component.html',
  styleUrl: './integrations.component.css'
})
export class IntegrationsComponent {

  userService: UserService = inject(UserService);
  authService: AuthService = inject(AuthService);
  tidalIntegration: TidalIntegrationService = inject(TidalIntegrationService);
  spotifyIntegration: IntegrationService = inject(SpotifyIntegrationService);

  allowedIntegrations: Record<IntegrationType, IntegrationService> = {
    [IntegrationType.SPOTIFY]: this.spotifyIntegration,
    [IntegrationType.TIDAL]: this.tidalIntegration,
  }
  userIntegrations: Set<IntegrationType> = new Set();
  userId: string | null = null;

  ngOnInit() {
    // TODO: generify this and fix typing
    this.tidalIntegration.registerIntegration();
    this.userId = this.authService.getUserId();
    if (this.userId) {
      this.userService.getUser(this.userId).subscribe(user => {
        this.userIntegrations = new Set(user.integrations);
      })
    }
  }

  statusOfAllowedIntegrations() {
    const integrations = Object.keys(this.allowedIntegrations) as IntegrationType[];
    return integrations.map(integration => ({
      name: integration,
      enabled: this.userIntegrations.has(integration),
    }));
  }

  integrateWithThirdParty(integration: IntegrationType) {
     const integrationService = this.allowedIntegrations[integration];
     integrationService.integrate();
  }

}
