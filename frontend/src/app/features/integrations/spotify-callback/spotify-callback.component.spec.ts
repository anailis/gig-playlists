import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifyCallbackComponent } from './spotify-callback.component';

describe('SpotifyCallbackComponent', () => {
  let component: SpotifyCallbackComponent;
  let fixture: ComponentFixture<SpotifyCallbackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpotifyCallbackComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpotifyCallbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
