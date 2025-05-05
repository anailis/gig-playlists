import { Component } from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf} from "@angular/common";
import {EventCardComponent} from "../../event-card/event-card.component";

interface Gig {
  day: string;
  date: number;
  month: string;
  year: number;
  title: string;
}

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [
    MatToolbar,
    NgForOf,
    EventCardComponent
  ],
  templateUrl: './gigs.component.html',
  styleUrl: './gigs.component.css'
})
export class GigsComponent {
  gigs: Gig[] = [
    { day: 'Mon', date: 30, month: 'December', year: 2025, title: 'blink-182 *' },
    { day: 'Sun', date: 31, month: 'December', year: 2025, title: 'Green Day *' },
    { day: 'Tue', date: 1, month: 'November', year: 2024, title: 'Everything Everything *' },
    { day: 'Wed', date: 2, month: 'November', year: 2025, title: 'The World is a Beautiful Place and I Am No Longer Afraid to Die *' },
    { day: 'Wed', date: 2, month: 'April', year: 2025, title: 'Cheekface' },
  ];

  groupedGigs: {
    year: number;
    months: {
      month: string;
      gigs: Gig[];
    }[];
  }[] = [];

  ngOnInit(): void {
    this.groupedGigs = this.groupByDate(this.gigs);
  }

  // TODO: ensure cards can be ordered in both asc and desc order
  groupByDate(gigs: Gig[]) {
    const yearMap: { [year: number]: { [month: string]: Gig[] } } = {};

    for (const gig of gigs) {
      if (!yearMap[gig.year]) {
        yearMap[gig.year] = {};
      }
      if (!yearMap[gig.year][gig.month]) {
        yearMap[gig.year][gig.month] = [];
      }

      yearMap[gig.year][gig.month].push(gig);
    }

    return Object.keys(yearMap)
        .sort() // sort years ascending
        .map(year => ({
          year: +year,
          months: Object.keys(yearMap[+year])
              .sort() // sort months alphabetically
              .map(month => ({
                month,
                gigs: yearMap[+year][month]
              }))
        }));
  }
}
