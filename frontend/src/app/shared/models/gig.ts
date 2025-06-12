export class Gig {
  artist: string;
  userId: string;
  spotifyArtistId: string;
  date: string;
  venue: string;
  year: number;
  month_name: string;
  month_number: number;
  day_of_month: number;
  day_of_week: string;

  constructor(data: { artist: string; userId: string; spotifyArtistId: string; date: string; venue: string }) {
    this.artist = data.artist;
    this.userId = data.userId;
    this.spotifyArtistId = data.spotifyArtistId;
    this.date = data.date;
    this.venue = data.venue;

    const parsedDate = new Date(data.date);
    this.year = parsedDate.getFullYear();
    this.month_name = parsedDate.toLocaleString('default', { month: 'long' });
    this.month_number = parsedDate.getMonth();
    this.day_of_month = parsedDate.getDate();
    this.day_of_week = parsedDate.toLocaleDateString('default', { weekday: 'short' });
  }
}
