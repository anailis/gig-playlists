import {Component, inject} from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf} from "@angular/common";
import {EventCardComponent} from "../event-card/event-card.component";
import {GigService} from "@core/services/gig.service";
import {Gig} from "@models/gig";

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [
    MatToolbar,
    NgForOf,
    EventCardComponent
  ],
  templateUrl: './gig-calendar.component.html',
  styleUrl: './gig-calendar.component.css'
})
export class GigCalendar {
  gigService = inject(GigService);

  gigs: Gig[] = [];

  groupedGigs: {
    year: number;
    months: {
      month: string;
      gigs: Gig[];
    }[];
  }[] = [];

  ngOnInit(): void {
    this.gigService.getGigsForUser("e60d3adf-1bd5-4b5e-b71c-42582ed86bd6").subscribe(
        (data: any[]) => {
          this.gigs = data.map(obj => new Gig(obj));
          this.groupedGigs = this.groupByDate(this.gigs);
        }
    );
  }

  // TODO: ensure cards can be ordered in both asc and desc order
    groupByDate(gigs: Gig[]) {
        const gigsByYear = this.groupByYear(gigs);

        return Object.keys(gigsByYear)
            .sort((a, b) => +a - +b)
            .map(year => {
                const gigsInYear = gigsByYear[+year];
                const months = this.groupByMonth(gigsInYear);

                const sortedMonths = Object.entries(months)
                    .sort((a, b) => a[1].monthNumber - b[1].monthNumber)
                    .map(([monthName, data]) => ({
                        month: monthName,
                        gigs: this.sortGigsByDay(data.gigs)
                    }));

                return {
                    year: +year,
                    months: sortedMonths
                };
            });
    }

    private groupByYear(gigs: Gig[]): { [year: number]: Gig[] } {
            return gigs.reduce((acc, gig) => {
                if (!acc[gig.year]) {
                    acc[gig.year] = [];
                }
                acc[gig.year].push(gig);
                return acc;
            }, {} as { [year: number]: Gig[] });
        }

    private groupByMonth(gigs: Gig[]): {
        [monthName: string]: { gigs: Gig[]; monthNumber: number }
    } {
        return gigs.reduce((acc, gig) => {
            if (!acc[gig.month_name]) {
                acc[gig.month_name] = {
                    gigs: [],
                    monthNumber: gig.month_number
                };
            }
            acc[gig.month_name].gigs.push(gig);
            return acc;
        }, {} as {
            [monthName: string]: { gigs: Gig[]; monthNumber: number }
        });
    }

    private sortGigsByDay(gigs: Gig[]): Gig[] {
        return gigs.slice().sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return dateA.getDate() - dateB.getDate(); // compare day of month
        });
    }
}
