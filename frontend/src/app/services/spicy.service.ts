import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SpicyService {

  http = inject(HttpClient);

  startGame(roomId: number, userId: string) {
    console.log('SpicyService: Starting game with roomId:', roomId, 'and userId:', userId);
    return this.http.post('/api/startgame', { roomId, userId }); }

}
