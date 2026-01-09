import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Gig } from '@models/gig';
import {environment} from "environments/environment";
import { DateTime } from "luxon";
import { Observable } from "rxjs";

/**
 * Responsible for retrieving and modifying Gig data
 * through interactions with the Gigs API.
 */
@Injectable({
  providedIn: 'root'
})
export class GigService {
  private http = inject(HttpClient);

  addGig(userId: string, artist: string, venue: string, spotifyArtistId: string, date: DateTime): void {
    const gig = new Gig({
      artist: artist,
      userId: 'USER#' + userId,
      date: date.toFormat("yyyy-MM-dd"),
      spotifyArtistId: spotifyArtistId,
      venue: venue,
    });

    this.http.post<Gig>(environment.gigsApiUrl + '/gigs', gig).subscribe(message => {
      console.log(message);
    });
  };

  deleteGig(gigId: string): Observable<Gig> {
    const stripped_id: string = gigId.replace(/^GIG#/, "");
    return this.http.delete<Gig>(environment.gigsApiUrl + '/gigs/' + stripped_id);
  }

  getGigsForUser(userId: string): Observable<Gig[]> {
    return this.http.get<Gig[]>(`${environment.gigsApiUrl}/users/${userId}/gigs`);
  }
}
