import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { details } from '../game_details';
import { WebSocketService } from '../services/web-socket.service';
import { Subscription } from 'rxjs/internal/Subscription';
import { WebSocketMessageTypes } from '../types';
import { PromptDialog } from '../shared/prompt-dialog/prompt-dialog';

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
  readonly gameKeys = Object.keys(details["games"])

  userName = localStorage.getItem('currentUser') ? JSON.parse(localStorage.getItem('currentUser')!).name : '';
  roomId = '';
  isModalOpen: boolean = false;
  selectedGameKey: string = '';
  pendingAction: null | 'create' | 'join' = null;
  roomCreateSub: Subscription | null = null;
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
    }

    this.roomCreateSub = this.websocketService.messageHandlers['createLobby'].subscribe(
      (message: WebSocketMessageTypes['createLobby']) => {
        this.roomId = message.roomId;
      }
    )
  }

  ngOnDestroy(): void {
    this.roomCreateSub?.unsubscribe();
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
    this.websocketService.sendMessage({
      type: 'userAuth',
      user_name: this.userService.displayName,
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
