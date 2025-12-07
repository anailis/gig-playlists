import {Component, inject, Input} from '@angular/core';
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";
import {GigService} from "@services/gig.service";

@Component({
  selector: 'app-event-card',
  standalone: true,
  imports: [
    MatIcon,
    MatIconButton,
    MatCard
  ],
  templateUrl: './event-card.component.html',
  styleUrl: './event-card.component.css'
})
export class EventCardComponent {
  @Input() id!: string | undefined;
  @Input() day!: string;
  @Input() date!: number;
  @Input() title!: string;

  gigService = inject(GigService);

  deleteGig() {
    if (this.id !== undefined) {
      this.gigService.deleteGig(this.id);
    }
  }

}
