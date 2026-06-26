import {Component, OnInit} from '@angular/core';
import {TidalIntegrationService} from "@services/tidal_integration.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-tidal-callback',
  standalone: true,
  imports: [],
  templateUrl: './tidal-callback.component.html',
  styleUrl: './tidal-callback.component.css'
})
export class TidalCallbackComponent implements OnInit {
  constructor(
      private tidalIntegrationService: TidalIntegrationService,
      private router: Router
  ) {}

  async ngOnInit() {

    await this.tidalIntegrationService.finaliseAuth();

    // immediately go back to the integrations page
    await this.router.navigate(['/integrations']);
  }

}
