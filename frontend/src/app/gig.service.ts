import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Gig } from './gig';
import { environment } from './config';
import { DateTime } from "luxon";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GigService {
  // TODO: change this URL to domain
  url = 'https://cjrpgycyf4.execute-api.eu-west-2.amazonaws.com/Prod';

  constructor(private http: HttpClient) {};

  addGig(artist: string, venue: string, spotifyArtistId: string, date: DateTime): void {

    let gig = new Gig({
      artist: artist,
      userId: 'USER#e60d3adf-1bd5-4b5e-b71c-42582ed86bd6',
      date: date.toFormat("yyyy-MM-dd"),
      spotifyArtistId: spotifyArtistId,
      venue: venue,
    });

    this.http.post<Gig>(this.url + '/gigs', gig, {
      headers: {
        'Authorization': environment.token
      }
    }).subscribe(message => {
      console.log(message);
    });
  };

  getGigsForUser(userId: string): Observable<Gig[]> {
    return this.http.get<Gig[]>(`${this.url}/users/${userId}/gigs`, {
      headers: {
        'Authorization': environment.token
      }
    })
  }
}
