import { Component } from '@angular/core';
import { AddGigFormComponent } from './add-gig-form/add-gig-form.component'

@Component({
  standalone: true,
  selector: 'app-component',
  templateUrl: './app.component.html',
  imports: [AddGigFormComponent]
})
export class AppComponent {
}
