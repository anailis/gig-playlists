import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GigsComponent } from './gigs.component';

describe('GigsComponent', () => {
  let component: GigsComponent;
  let fixture: ComponentFixture<GigsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GigsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GigsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
