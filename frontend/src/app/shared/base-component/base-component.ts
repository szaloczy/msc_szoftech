import { Directive, inject, OnDestroy } from '@angular/core';
import { WebSocketService } from '../../services/web-socket.service';
import { ActivatedRoute, Router } from '@angular/router';

@Directive()
export abstract class BaseComponent implements OnDestroy {
  protected webSocketService = inject(WebSocketService);
  private readonly activetedRoute = inject(ActivatedRoute);
  protected readonly router = inject(Router);
  roomId: string | null = null;

  constructor() {
    this.activetedRoute.paramMap.subscribe(params => {
      this.roomId = params.get('roomId') ?? '';
      if (this.roomId) {
        this.webSocketService.sendMessage({ type: 'roomJoin', room_id: this.roomId });
      } else {
        this.router.navigate(['/home']);
      }
    });
  }

  ngOnDestroy() {
    this.webSocketService.unsubscribeComponent(this);
  }
}
