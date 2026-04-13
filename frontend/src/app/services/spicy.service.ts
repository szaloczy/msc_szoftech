import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SpicyService {

  http = inject(HttpClient);

  startGame(roomId: number) { return this.http.post('/api/startgame', { roomId }); }

}
