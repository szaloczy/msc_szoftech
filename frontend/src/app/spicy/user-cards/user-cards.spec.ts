import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserCards } from './user-cards';

describe('UserCards', () => {
  let component: UserCards;
  let fixture: ComponentFixture<UserCards>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCards]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserCards);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
