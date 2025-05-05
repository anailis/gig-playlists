import {Component, Input} from '@angular/core';
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {MatCard} from "@angular/material/card";

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
  @Input() day!: string;
  @Input() date!: number;
  @Input() title!: string;

}
