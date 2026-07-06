import {Component, inject, ChangeDetectionStrategy} from '@angular/core';
import {TidalAPIService} from "@services/tidal_api.service";

@Component({
    selector: 'app-playlists',
    imports: [],
    templateUrl: './playlists.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './playlists.component.css'
})
export class PlaylistsComponent {
  tidalApiService = inject(TidalAPIService);

  seeAlbum() {
    this.tidalApiService.seeAlbum();
  }

}
