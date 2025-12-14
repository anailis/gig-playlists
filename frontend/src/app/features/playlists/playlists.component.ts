import {Component, inject} from '@angular/core';
import {TidalAuthService} from "@services/tidal_auth.service";

@Component({
  selector: 'app-playlists',
  standalone: true,
  imports: [],
  templateUrl: './playlists.component.html',
  styleUrl: './playlists.component.css'
})
export class PlaylistsComponent {
  tidalService = inject(TidalAuthService);

  ngOnInit(): void {
  }

  loginToTidal() {
    this.tidalService.login();
  }

}
