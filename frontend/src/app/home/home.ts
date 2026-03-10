import {Component, inject, OnInit} from '@angular/core';
import { GameMode } from '../types';
import {UserService} from '../services/user.service';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import { details } from '../game_details';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ FormsModule, CommonModule ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit{
  userService = inject(UserService);
  games : GameMode[] =[
    { id: '1', name: 'Spicy', description: 'card games with a spicy twist', duration: '30 mins', player: 4 },
    { id: '2', name: 'Uno', description: 'classic card game with colorful cards', duration: '20 mins', player: 4 },
    { id: '3', name: 'Blackjack', description: 'popular casino card game', duration: '15 mins', player: 2 },
  ]

  readonly gameKeys = Object.keys(details["games"])

  newUsername: string = '';
  isModalOpen: boolean = false;
  selectedGameKey: string = '';
  isGameDetailsSidebarOpen: boolean = false;

  ngOnInit(): void {}

  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
    this.newUsername = '';
  }

  saveUser() {
    if (this.newUsername.trim().length >= 3 && this.newUsername.trim().length <= 50) {
      this.userService.createUser(this.newUsername.trim()).subscribe({
        next: () => {
          this.closeModal();
        },
        error: (err) => console.error('Error while creating user:', err)
      });
    }
  }

  selectGame(gameKey: string) {
    this.isGameDetailsSidebarOpen = !this.isGameDetailsSidebarOpen;
    this.selectedGameKey = gameKey;
  }

  getGameDetails(key: string) {
    return details.games[key as keyof typeof details.games];
  }

}
