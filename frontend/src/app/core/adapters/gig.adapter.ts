import {Injectable} from "@angular/core";
import {Gig} from "@models/gig";

/**
 * Responsible for mapping Gig data
 * to structures better for UI display.
 */
@Injectable({
    providedIn: 'root'
})
export class GigAdapter {

    groupByYear(gigs: Gig[]): { [year: number]: Gig[] } {
        return gigs.reduce((acc, gig) => {
            if (!acc[gig.year]) {
                acc[gig.year] = [];
            }
            acc[gig.year].push(gig);
            return acc;
        }, {} as { [year: number]: Gig[] });
    }
}