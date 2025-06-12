import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

import { MatLuxonDateModule } from '@angular/material-luxon-adapter';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { DateTime } from 'luxon';

import { GigService } from '@services/gig.service';

@Component({
  standalone: true,
  selector: 'gig-form',
  templateUrl: './gig-form.component.html',
  imports: [ReactiveFormsModule, MatFormFieldModule, MatInputModule,
    MatButtonModule, MatDatepickerModule, MatLuxonDateModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GigFormComponent {
  gigService = inject(GigService);
  gigForm = new FormGroup({
    artist: new FormControl('', Validators.required),
    venue: new FormControl('', Validators.required),
    spotifyArtistId: new FormControl('', Validators.required),
    date: new FormControl<DateTime | null>(null, Validators.required),
  });

  onSubmit() {
    // is this the best way to do this?
    this.gigService.addGig(
      this.gigForm.value.artist ?? '',
      this.gigForm.value.venue ?? '',
      this.gigForm.value.spotifyArtistId ?? '',
      this.gigForm.value.date ?? DateTime.now(),
    );
  }
}
