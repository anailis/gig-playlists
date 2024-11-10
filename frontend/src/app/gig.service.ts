import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Gig } from './gig';
import { environment } from './config';

@Injectable({
  providedIn: 'root'
})
export class GigService {
  // TODO: Retrieve this URL?
  url = 'https://cjrpgycyf4.execute-api.eu-west-2.amazonaws.com/Prod/gigs';

  constructor(private http: HttpClient) {};

  addGig(artist: string, venue: string, spotifyArtistId: string, date: string): void {
    let gig: Gig = {
      artist: artist,
      userId: 'USER#e60d3adf-1bd5-4b5e-b71c-42582ed86bd6',
      date: date,
      spotifyArtistId: spotifyArtistId,
      venue: venue,
    };
    console.log(gig);
    this.http.post<Gig>(this.url, gig, {
      headers: {
        'Authorization': environment.token
      }
    }).subscribe(message => {
      console.log(message);
    });
  };
}
