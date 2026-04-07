import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Spicy } from './spicy';

describe('Spicy', () => {
  let component: Spicy;
  let fixture: ComponentFixture<Spicy>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Spicy]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Spicy);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
