import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GigCalendar } from './gig-calendar.component';

describe('GigsComponent', () => {
  let component: GigCalendar;
  let fixture: ComponentFixture<GigCalendar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GigCalendar]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GigCalendar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
