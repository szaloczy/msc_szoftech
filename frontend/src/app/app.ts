import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { WebSocketService } from './services/web-socket.service';
import { UserService } from './services/user.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private readonly webSocketService = inject(WebSocketService);
  userService = inject(UserService);
  ngOnInit(): void {
    this.webSocketService.connect();
  }
}
