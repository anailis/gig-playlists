import {Component, inject} from '@angular/core';
import {TidalIntegrationService} from "@services/tidal_integration.service";
import {TidalAPIService} from "@services/tidal_api.service";

@Component({
  selector: 'app-playlists',
  standalone: true,
  imports: [],
  templateUrl: './playlists.component.html',
  styleUrl: './playlists.component.css'
})
export class PlaylistsComponent {
  tidalAuthService = inject(TidalIntegrationService);
  tidalApiService = inject(TidalAPIService);

  async ngOnInit() {
  }

  seeAlbum() {
    this.tidalApiService.seeAlbum();
  }

}
