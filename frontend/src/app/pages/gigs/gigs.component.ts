import { Component } from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [
    MatIcon,
    MatIconButton,
    MatToolbar,
    MatCard,
    NgForOf
  ],
  templateUrl: './gigs.component.html',
  styleUrl: './gigs.component.css'
})
export class GigsComponent {
  gigs = [
    { day: 'Mon', date: 30, month: 'December', title: 'blink-182 *' },
    { day: 'Sun', date: 31, month: 'December', title: 'Green Day *' },
    { day: 'Tue', date: 1, month: 'November', title: 'Everything Everything *' },
    { day: 'Wed', date: 2, month: 'November', title: 'The World is a Beautiful Place and I Am No Longer Afraid to Die *' },
  ];
}
