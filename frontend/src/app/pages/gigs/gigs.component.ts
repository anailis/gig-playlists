import { Component } from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatList, MatListItem} from "@angular/material/list";
import {MatIcon} from "@angular/material/icon";
import {MatIconButton} from "@angular/material/button";
import {MatLine} from "@angular/material/core";
import {MatCard} from "@angular/material/card";

@Component({
  selector: 'app-gigs',
  standalone: true,
  imports: [
    MatIcon,
    MatIconButton,
    MatToolbar,
    MatCard
  ],
  templateUrl: './gigs.component.html',
  styleUrl: './gigs.component.css'
})
export class GigsComponent {

}
