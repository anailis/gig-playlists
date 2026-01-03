import {Component, inject} from '@angular/core';
import {NgForOf} from "@angular/common";
import {MatCard, MatCardContent} from "@angular/material/card";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {IntegrationType} from "@models/user";

@Component({
  selector: 'app-playlists',
  standalone: true,
  imports: [
    NgForOf,
    MatCard,
    MatButton,
    MatIcon,
    MatCardContent
  ],
  templateUrl: './integrations.component.html',
  styleUrl: './integrations.component.css'
})
export class IntegrationsComponent {

  async ngOnInit() {
  }

  integrationTypes =  Object.keys(IntegrationType);

}
