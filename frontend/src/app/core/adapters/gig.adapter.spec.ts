import {GigAdapter} from "@core/adapters/gig.adapter";
import {Gig} from "@models/gig";

describe('GigAdapter', () => {
   let gigAdapter: GigAdapter;

   beforeEach(() => {
       gigAdapter = new GigAdapter();
   })

   it('should group gigs by year', () => {
      const gig_2025 = new Gig({artist: 'artist', userId: 'userId', spotifyArtistId: 'id', date: '2025-05-03', venue: 'venue'});
      const gig_1977 = new Gig({artist: 'artist', userId: 'userId', spotifyArtistId: 'id', date: '1977-06-03', venue: 'venue'});
      const gig_2023A = new Gig({artist: 'artist', userId: 'userId', spotifyArtistId: 'id', date: '2023-05-03', venue: 'venue'});
      const gig_2023B = new Gig({artist: 'artist', userId: 'userId', spotifyArtistId: 'id', date: '2023-06-08', venue: 'venue'});
      const gigs = [
          gig_2023A,
          gig_2025,
          gig_2023B,
          gig_1977
      ]

       const grouped = gigAdapter.groupByYear(gigs)
       expect(Object.keys(grouped).length).toEqual(3);
       expect(grouped["2025"]).toEqual([gig_2025]);
       expect(grouped["1977"]).toEqual([gig_1977]);
       expect(grouped["2023"]).toEqual([gig_2023A, gig_2023B]);
   });
});