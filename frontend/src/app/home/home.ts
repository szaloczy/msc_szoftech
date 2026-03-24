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

  isModalOpen: boolean = false;
  selectedGameKey: string = '';
  pendingAction: null | 'create' | 'join' = null;

  ngOnInit(): void {}

  createRoom() {
    this.websocketService.sendMessage({
      type: 'auth',
      username: this.userService.displayName,
      user_id: this.userService.currentUser()?.id
    });
    this.websocketService.sendMessage(
        { 
          type: 'createLobby',
          game: this.selectedGameKey
        }
    );
    this.pendingAction = null;
  }

  joinRoom() {
    this.websocketService.sendMessage({
      type: 'auth',
      username: this.userService.displayName,
      user_id: this.userService.currentUser()?.id
    });
    //TODO: implement join room logic
    this.pendingAction = null;
  }

  selectGame(gameKey: string) {
    this.selectedGameKey = gameKey;
  }

  getGameDetails(key: string) {
    return details.games[key as keyof typeof details.games];
  }

}
