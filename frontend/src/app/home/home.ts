import { Component } from '@angular/core';
import { GameMode } from '../types';

@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  games : GameMode[] =[
    { id: '1', name: 'Spicy', description: 'card games with a spicy twist', duration: '30 mins', player: 4 },
    { id: '2', name: 'Uno', description: 'classic card game with colorful cards', duration: '20 mins', player: 4 },
    { id: '3', name: 'Blackjack', description: 'popular casino card game', duration: '15 mins', player: 2 },
  ]

  

}
