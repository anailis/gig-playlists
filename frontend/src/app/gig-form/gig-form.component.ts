import { Component } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'gig-form',
  templateUrl: './gig-form.component.html',
  imports: [ReactiveFormsModule],
})
export class GigFormComponent {
  gigForm = new FormGroup({
    artist: new FormControl('', Validators.required),
    venue: new FormControl('')
  });

  onSubmit() {
    console.warn(this.gigForm.value);
  }
}
