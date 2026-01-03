import {Component, inject} from '@angular/core';
import {TidalAuthService} from "@services/tidal_auth.service";
import {TidalAPIService} from "@services/tidal_api.service";

@Component({
  selector: 'app-playlists',
  standalone: true,
  imports: [],
  templateUrl: './playlists.component.html',
  styleUrl: './playlists.component.css'
})
export class PlaylistsComponent {
  tidalAuthService = inject(TidalAuthService);
  tidalApiService = inject(TidalAPIService);

  async ngOnInit() {
    await this.tidalAuthService.finaliseLogin();
  }

  loginToTidal() {
    this.tidalAuthService.login();
  }

  seeAlbum() {
    this.tidalApiService.seeAlbum();
  }

}
