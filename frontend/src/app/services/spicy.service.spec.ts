import { TestBed } from '@angular/core/testing';

import { SpicyService } from './spicy.service';

describe('SpicyService', () => {
  let service: SpicyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpicyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
