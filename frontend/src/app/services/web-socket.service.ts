import { Injectable, signal } from '@angular/core';
import { BehaviorSubject, Subject, Subscription } from 'rxjs';
import { websocketMessageSchemaTypes, WebSocketMessageTypes } from '../types';
import { ZodLiteral } from 'zod';

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

  messageHandlers: {
    [K in keyof WebSocketMessageTypes]: Subject<WebSocketMessageTypes[K]>;
  } = Object.keys(websocketMessageSchemaTypes).reduce((handlers, key) => {
    handlers[key as keyof WebSocketMessageTypes] = new Subject();
    return handlers;
  }, [] as any);


  connect() {
    this.connectionReady.next(false);
    this.socket = new WebSocket('/ws');

    this.socket.onopen = () => {
      this.connectionReady.next(true);
      console.log('WebSocket connection established');
    };

   this.socket.onmessage = (event) => {
      console.log('Received message:', event.data);
      try {
        const message = JSON.parse(event.data);

        if(!message.type) {
          throw new Error('Message type is missing from the payload');
        }

        const relatedType = Object.entries(websocketMessageSchemaTypes).find(
          ([, schema]) => (schema.shape.type as ZodLiteral<string>).value === message.type
        );

        if(relatedType) {
          const messageType = relatedType[0] as keyof WebSocketMessageTypes;
          const schema = websocketMessageSchemaTypes[messageType];
          const result = schema.safeParse(message);

          if (result.success) {
            this.messageHandlers[messageType].next(result.data as any);
          }
        }

      } catch (error) {
        console.error('Failed to parse WebSocket message:', event.data, error);
      }
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

  private authUser() {
    const userId = localStorage.getItem('userId');
    const userName = localStorage.getItem('userName');
    if (userId && userName && userName.length > 2) {
      this.sendMessage({
        type: 'userAuth',
        'user_id': userId
      });
    }
  }
}
