import { Component } from '@angular/core';
import {MatListItem, MatListItemIcon, MatListItemTitle, MatNavList} from "@angular/material/list";
import {MatIcon} from "@angular/material/icon";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-authbar',
  standalone: true,
    imports: [
        MatNavList,
        MatIcon,
        MatListItemIcon,
        MatListItemTitle,
        MatListItem
    ],
  templateUrl: './authbar.component.html',
  styleUrl: './authbar.component.css'
})
export class AuthbarComponent {

}
