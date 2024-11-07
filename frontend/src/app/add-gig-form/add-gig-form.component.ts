import { Component } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'add-gig-form',
  templateUrl: './add-gig-form.component.html',
  imports: [ReactiveFormsModule],
})
export class AddGigFormComponent {
  gigForm = new FormGroup({
    artist: new FormControl('', Validators.required),
    venue: new FormControl('')
  });

  onSubmit() {
    console.warn(this.gigForm.value);
  }
}
