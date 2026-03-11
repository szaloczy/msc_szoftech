import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  private socket: WebSocket | null = null;
  private readonly RECONNECTIONTERVAL = 5000; // 5 sec
  private connectionReady = new BehaviorSubject<boolean>(false);
  public connectionReady$ = this.connectionReady.asObservable();

  public get isConnectionReady(): boolean {
    return this.connectionReady.value;  
  }

    //Some kind of message handler for shcema type messages
    /*
    messageHnadlers = {}
    */

   connect() {
    this.connectionReady.next(false);
    this.socket = new WebSocket('/ws');
    
    this.socket.onopen = () => {
      this.connectionReady.next(true);
      console.log('WebSocket connection established');
    };
    
   this.socket.onmessage = (event) => {
      console.log('Received message:', event.data);
      // Handle incoming messages here
    };


    this.socket.onclose = () => {
      this.connectionReady.next(false);
      this.reconnect();
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.connectionReady.next(false);
    };
  }

  private reconnect() {
    setTimeout(() => {
      console.log("Lost Websocket. Reconnecting...");
      this.connect();
    }, this.RECONNECTIONTERVAL);
  }

  public sendMessage(message: object) {
    if(!this.socket) {
      console.error('WebSocket is not initialized');
      return;
    }

    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('Websocket is not open. Ready state: ', this.socket.readyState);
    } 
  }
}
