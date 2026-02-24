import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  socket: WebSocket | null = null;

  private _serverMessage = signal('');
  readonly serverMessage = this._serverMessage.asReadonly();

  connect() {
    this.socket = new WebSocket('ws://localhost:8765');

    

    this.socket.onopen = () => {
      console.log('WebSocket connection opened');
    }

    this.socket.onmessage = (msg) => {
      this._serverMessage.set(String(msg.data));
    }

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    }
  }

  sendMessage(message: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    } else {
      console.error('WebSocket is not open. Unable to send message.');
    }
  }
}
