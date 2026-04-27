import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { details } from '../game_details';
import { WebSocketService } from '../services/web-socket.service';
import { Subscription } from 'rxjs/internal/Subscription';
import { WebSocketMessageTypes } from '../types';
import { PromptDialog } from '../shared/prompt-dialog/prompt-dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ FormsModule, CommonModule, PromptDialog ],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit, OnDestroy {

  private readonly userService = inject(UserService);
  private readonly websocketService = inject(WebSocketService);
  private readonly router = inject(Router);
  readonly gameKeys = Object.keys(details["games"])

  userName = localStorage.getItem('currentUser') ? JSON.parse(localStorage.getItem('currentUser')!).name : '';
  roomId = '';
  isModalOpen: boolean = false;
  selectedGameKey: string = '';
  pendingAction: null | 'create' | 'join' = null;
  loobyCreateSub: Subscription | null = null;
  joinLobbyRoomSub: Subscription | null = null;
  showPromptDialog = false;
  isAuthenticated = false;

  get displayUserName(): string {
    return this.userName?.trim() ? this.userName : 'guest';
  }

  ngOnInit(): void {
    this.websocketService.connect();

    if (!this.userName) {
      this.userName = 'guest'
      this.isAuthenticated = false;
    } else {
      this.isAuthenticated = true;
      this.websocketService.connectionReady$.subscribe(ready => {
        if (ready) this.userService.startAuthProcess();
      });
    }

    this.loobyCreateSub = this.websocketService.messageHandlers['createLobby'].subscribe(
      (message: WebSocketMessageTypes['createLobby']) => {
        this.roomId = message.roomId;
        if (this.roomId) {
          localStorage.setItem('roomId', this.roomId);
          this.router.navigate([`/${this.selectedGameKey}/${this.roomId}`]);
        }
      }
    );
  }

  ngOnDestroy(): void {
    this.loobyCreateSub?.unsubscribe();
    this.joinLobbyRoomSub?.unsubscribe();
  }

  createRoom() {
    this.pendingAction = 'create';
    if (this.isAuthenticated) {
      this.websocketService.sendMessage({
        type: 'createLobby',
        game: this.selectedGameKey,
        user_id: this.userService.currentUser()?.id
      });
      this.showPromptDialog = false;
    } else {
      this.showPromptDialog = true;
    }
  }

  joinRoom() {
    this.pendingAction = 'join';
    if (this.isAuthenticated) {
      this.websocketService.sendMessage({
        type: 'joinLobby',
        room_id: this.roomId
      });

      this.websocketService.messageHandlers.join.subscribe({
        next: (data) => {
          const gameType = data.gameType;
          console.log('Joining lobby:', data, gameType);
          const roomId = data.roomId;
          console.log('Navigating to room:', roomId, gameType);
          this.router.navigate([`/${gameType}/${roomId}`]);
          this.showPromptDialog = false;
        },
        error: (err) => {
          console.error(err);
        }
      });
    } else {
      this.showPromptDialog = true;
    }
  }

  selectGame(gameKey: string) {
    this.selectedGameKey = gameKey;
  }

  getGameDetails(key: string) {
    return details.games[key as keyof typeof details.games];
  }

  onDialogConfirmed(name: string) {
    this.userName = name.trim();
    if (this.userName.length > 2) {
      this.userService.createUser(this.userName).subscribe({
        next: (res) => {
          if (!res.success || !res.data) {
            this.showPromptDialog = true;
            return;
          }

          const user = res.data;
          this.isAuthenticated = true;

          this.websocketService.sendMessage({
            type: 'userAuth',
            user_name: user.name,
            user_id: user.id
          });

          if (this.pendingAction === 'create') {
            this.createRoom();
            this.showPromptDialog = false;
          } else if (this.pendingAction === 'join') {
            this.joinRoom();
            this.showPromptDialog = false;
          }
        },
        error: (err) => {
          console.error(err);
          this.showPromptDialog = true;
        }
      });

    } else {
      alert('Username must be at least 2 character');
    }
  }

  onDialogCanceled() {
    this.showPromptDialog = false;
  }

}
