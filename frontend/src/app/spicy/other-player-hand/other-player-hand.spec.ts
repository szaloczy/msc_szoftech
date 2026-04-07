import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OtherPlayerHand } from './other-player-hand';

describe('OtherPlayerHand', () => {
  let component: OtherPlayerHand;
  let fixture: ComponentFixture<OtherPlayerHand>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OtherPlayerHand]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OtherPlayerHand);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
