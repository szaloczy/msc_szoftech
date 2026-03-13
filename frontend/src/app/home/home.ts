import {Component, inject, OnInit, signal} from '@angular/core';
import { GameMode } from '../types';
import {UserService} from '../services/user.service';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import { details } from '../game_details';
import { WebSocketService } from '../services/web-socket.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ FormsModule, CommonModule ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {

  userService = inject(UserService);
  websocketService = inject(WebSocketService);

  readonly gameKeys = Object.keys(details["games"])
  readonly isAuthenticated = signal(false);

  username: string = '';
  isModalOpen: boolean = false;
  selectedGameKey: string = '';
  isGameDetailsSidebarOpen: boolean = false;
  pendingAction: null | 'create' | 'join' = null;

  ngOnInit(): void {}

  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
    this.username = '';
  }

  saveUser() {
    if (this.username.trim().length >= 3 && this.username.trim().length <= 50) {
      this.userService.createUser(this.username.trim()).subscribe({
        next: () => {
          this.isAuthenticated.set(true);

          this.websocketService.sendMessage({
            type: 'auth',
            username: this.username.trim(),
            user_id: this.userService.currentUser()?.id
          });

          if (this.pendingAction === 'create') {
            this.createRoom();
          } else if (this.pendingAction === 'join') {
            this.joinRoom();
          }

          this.pendingAction = null;
          this.closeModal();
        },
        error: (err) => console.error('Error while creating user:', err)
      });
    }
  }

  createRoom() {
    if (this.isAuthenticated()) {
      this.websocketService.sendMessage(
        { 
          type: 'createLobby',
          game: this.selectedGameKey
        }
      );

    } else {
      this.pendingAction = 'create';
      this.openModal();
    }
  }

  joinRoom() {
    //TODO: implement join room logic
  }

  selectGame(gameKey: string) {
    this.isGameDetailsSidebarOpen = !this.isGameDetailsSidebarOpen;
    this.selectedGameKey = gameKey;
  }

  getGameDetails(key: string) {
    return details.games[key as keyof typeof details.games];
  }

}
