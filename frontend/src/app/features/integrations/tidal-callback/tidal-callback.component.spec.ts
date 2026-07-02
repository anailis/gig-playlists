import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TidalCallbackComponent } from './tidal-callback.component';

describe('TidalCallbackComponent', () => {
  let component: TidalCallbackComponent;
  let fixture: ComponentFixture<TidalCallbackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TidalCallbackComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TidalCallbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
