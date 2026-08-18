import {ChangeDetectionStrategy, Component, inject, Inject, OnInit} from '@angular/core';

import {MatCard, MatCardContent} from "@angular/material/card";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {IntegrationType} from "@models/user";
import {UserService} from "@services/user.service";
import {AuthService} from "@services/auth.service";
import {IntegrationService} from "@services/integration.service";
import {INTEGRATION_SERVICES,} from "@features/integrations/integrations.tokens";

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
        @Inject(INTEGRATION_SERVICES)
        private readonly integrationServices: IntegrationService[],
    ) {
        this.allowedIntegrations = new Map(
            integrationServices.map(service => [service.getAppName(), service])
        );
    }

  ngOnInit() {
    this.userId = this.authService.getUserId();
    if (this.userId) {
      this.userService.getUser(this.userId).subscribe(user => {
        const userIntegrations = new Set(user.integrations);
        const integrations = Array.from(this.allowedIntegrations.keys());
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
