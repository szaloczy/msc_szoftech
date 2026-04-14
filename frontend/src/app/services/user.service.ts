import { inject, Injectable, signal } from '@angular/core';

import { tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { UserApiResponse, User } from '../types';
import { WebSocketService } from './web-socket.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private readonly STORAGE_KEY = 'currentUser';
  private readonly websocketService = inject(WebSocketService);
  private readonly http = inject(HttpClient);

  readonly currentUser = signal<User | null>(this.loadFromStorage());

  get displayName(): string {
    console.log('Current user:', this.currentUser());
    return this.currentUser()?.name ?? 'Guest';
  }

  createUser(username: string) {
    return this.http
      .post<UserApiResponse>('http://localhost:5000/api/users', { username })
      .pipe(
        tap((res) => {
          if (res.success && res.data) {
            this.saveUser(res.data);
          }
        })
      );
  }

  startAuthProcess() {
      const { id, name } = this.currentUser() || {};

      if(id && name && name.length >= 3) {
        this.websocketService.sendMessage({
          type: 'userAuth',
          user_id: id,
          user_name: name
      });
    } else {
      localStorage.removeItem("currentUser");
    }
  }

  clearUser(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    this.currentUser.set(null);
  }

  private saveUser(user: User): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(user));

    this.currentUser.set(user);
  }

  private loadFromStorage(): User | null {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    return stored ? (JSON.parse(stored) as User) : null;

  }
}
