import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GigService {
  url = '';

  constructor(private http: HttpClient) {};

  addGig(artist: String, venue: String) {
  };
}
