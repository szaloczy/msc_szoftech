import { Component, inject, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { WebSocketService } from './services/web-socket.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  socketService = inject(WebSocketService);
  serverMessage = '';

  ngOnInit() {
    this.socketService.connect();
  }

  sendMessage() {
    this.socketService.sendMessage('Hello from Angular!');
  }
}
