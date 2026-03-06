import {Injectable, signal} from '@angular/core';

import {tap} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {UserApiResponse, User} from '../types';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private readonly STORAGE_KEY = 'currentUser';

  readonly currentUser = signal<User | null>(this.loadFromStorage());

  constructor(private http: HttpClient) {}

  get displayName(): string {
    return this.currentUser()?.name ?? 'Guest';
  }

  createUser(name: string) {
    return this.http
      .post<UserApiResponse>('http://localhost:5000/api/users', { name })
      .pipe(
        tap((res) => {
          if (res.success && res.data) {
            this.saveUser(res.data);
          }
        })
      );
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
