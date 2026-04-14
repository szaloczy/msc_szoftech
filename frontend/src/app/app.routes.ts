import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Board } from './spicy/board/board';
import { UserCards } from './spicy/user-cards/user-cards';

export const routes: Routes = [
    { path: 'home', component: Home },
    { path: 'usercard', component: UserCards },
    { path: 'spicy/:roomId', component: Board },
    { path: '**', redirectTo: '/home' },
];
