import { Component, inject } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { GigService } from '../gig.service';

@Component({
  standalone: true,
  selector: 'gig-form',
  templateUrl: './gig-form.component.html',
  imports: [ReactiveFormsModule],
})
export class GigFormComponent {
  gigService = inject(GigService);
  gigForm = new FormGroup({
    artist: new FormControl('', Validators.required),
    venue: new FormControl(''),
    spotifyArtistId: new FormControl(''),
    date: new FormControl(''),
  });

  onSubmit() {
    this.gigService.addGig(
      this.gigForm.value.artist ?? '',
      this.gigForm.value.venue ?? '',
      this.gigForm.value.spotifyArtistId ?? '',
      this.gigForm.value.date ?? '',
    );
  }
}
