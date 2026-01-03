import {Component, inject} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {MatCard, MatCardContent} from "@angular/material/card";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {IntegrationType} from "@models/user";
import {UserService} from "@services/user.service";
import {AuthService} from "@services/auth.service";

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

  allowedIntegrations: IntegrationType[] = Object.values(IntegrationType);
  userIntegrations: Set<IntegrationType> = new Set();
  userId: string | null = null;
  userService: UserService = inject(UserService);
  authService: AuthService = inject(AuthService);

  async ngOnInit() {
    this.userId = this.authService.getUserId();
    if (this.userId) {
      this.userService.getUser(this.userId).subscribe(user => {
        this.userIntegrations = new Set(user.integrations);
        console.log(this.userIntegrations);
      })
    }
  }

  statusOfAllowedIntegrations() {
    return this.allowedIntegrations.map(integration => ({
      name: integration,
      enabled: this.userIntegrations.has(integration),
    }));
  }

}
