
import { Component, inject, OnInit, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { WebSocketService } from './services/web-socket.service';
import { UserService } from './services/user.service';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { WebSocketMessageTypes } from './types';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App implements OnInit {
  webSocketService = inject(WebSocketService);
  userService = inject(UserService);
  router = inject(Router);
  httpClient = inject(HttpClient);

  isAuthenticated = false;
  showRainingEffect = false;
  lastErrorMessage = '';
  lastNotiMessage = '';
  isDevTool = true;

  // Dialog properties
  showPromptDialog = false;
  promptTitle = '';
  promptMessage = '';
  promptDefaultValue = '';
  promptPlaceholder = '';
  promptDialogType = '';

  constructor() {
    this.webSocketService.connect();
  }

  ngOnInit() {
    this.webSocketService.messageHandlers['auth'].subscribe(
      (message: WebSocketMessageTypes['auth']) => {
      this.isAuthenticated = message.success;
    });
  }
}
