import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Gig } from '@models/gig';
import { environment } from '../../config';
import { DateTime } from "luxon";
import { Observable } from "rxjs";

/**
 * Responsible for retrieving Gig data
 * through interactions with the Gigs API.
 */
@Injectable({
  providedIn: 'root'
})
export class GigService {
  constructor(private http: HttpClient) {};

  addGig(artist: string, venue: string, spotifyArtistId: string, date: DateTime): void {

    let gig = new Gig({
      artist: artist,
      userId: 'USER#e60d3adf-1bd5-4b5e-b71c-42582ed86bd6',
      date: date.toFormat("yyyy-MM-dd"),
      spotifyArtistId: spotifyArtistId,
      venue: venue,
    });

    this.http.post<Gig>(environment.gigsApiUrl + '/gigs', gig, {
      headers: {
        'Authorization': environment.token
      }
    }).subscribe(message => {
      console.log(message);
    });
  };

  getGigsForUser(userId: string): Observable<Gig[]> {
    return this.http.get<Gig[]>(`${environment.gigsApiUrl}/users/${userId}/gigs`, {
      headers: {
        'Authorization': environment.token
      }
    })
  }
}
