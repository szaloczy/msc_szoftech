import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { WebSocketService } from './services/web-socket.service';
import { UserService } from './services/user.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  username = ''
  private readonly webSocketService = inject(WebSocketService);
  userService = inject(UserService);
  userNameProvided = signal(false);

  loading = signal(true);



  ngOnInit(): void {
    if (this.userService.currentUser()) {
      this.userNameProvided.set(true);
    }
    this.webSocketService.connect();
    this.loading.set(false);
  }



  saveUser() {
    if (this.username.trim().length >= 3 && this.username.trim().length <= 50) {
      this.loading.set(true);
      this.userService.createUser(this.username.trim()).subscribe({
        next: () => {
          this.userNameProvided.set(true);
          this.loading.set(false);
        },
        error: (err) =>{
           console.error('Error while creating user:', err)
           this.loading.set(false);
        }
        
      });
    }
  }
}