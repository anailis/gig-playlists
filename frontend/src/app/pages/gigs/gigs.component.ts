import { Component } from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";
import {NgForOf} from "@angular/common";
import {EventCardComponent} from "../../event-card/event-card.component";

interface Gig {
  day: string;
  date: number;
  month: string;
  title: string;
}

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [
    MatIcon,
    MatIconButton,
    MatToolbar,
    MatCard,
    NgForOf,
    EventCardComponent
  ],
  templateUrl: './gigs.component.html',
  styleUrl: './gigs.component.css'
})
export class GigsComponent {
  gigs: Gig[] = [
    { day: 'Mon', date: 30, month: 'December', title: 'blink-182 *' },
    { day: 'Sun', date: 31, month: 'December', title: 'Green Day *' },
    { day: 'Tue', date: 1, month: 'November', title: 'Everything Everything *' },
    { day: 'Wed', date: 2, month: 'November', title: 'The World is a Beautiful Place and I Am No Longer Afraid to Die *' },
  ];

  gigsByMonth: { month: string; gigs: Gig[] }[] = [];

  ngOnInit(): void {
    this.gigsByMonth = this.groupByMonth(this.gigs);
  }

  groupByMonth(gigs: Gig[]): { month: string; gigs: Gig[] }[] {
    const groups: { [month: string]: Gig[]} = {};

    for (const gig of gigs) {
      if (!groups[gig.month]) {
        groups[gig.month] = [];
      }
      groups[gig.month].push(gig);
    }

    return Object.keys(groups).map(month => ({
      month,
      gigs: groups[month]
    }));
  }
}
