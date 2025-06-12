import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventCardComponent } from './event-card.component';

fdescribe('EventCardComponent', () => {
  let component: EventCardComponent;
  let fixture: ComponentFixture<EventCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EventCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EventCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render input values correctly', () => {
    component.day = 'Monday';
    component.date = 12;
    component.title = 'Team Meeting';
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[data-testid="title"]')?.textContent).toContain('Team Meeting');
    expect(compiled.querySelector('[data-testid="day"]')?.textContent).toContain('Monday');
    expect(compiled.querySelector('[data-testid="date"]')?.textContent).toContain('12');
  });
});
