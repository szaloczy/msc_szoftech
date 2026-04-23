import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-other-player-hand',
  imports: [CommonModule],
  templateUrl: './other-player-hand.html',
  styleUrl: './other-player-hand.css',
})
export class OtherPlayerHand {
    @Input() name = '';
    @Input() cards = 0;

    getRotation(index: number): number {
      const total = Math.min(this.cards,5);
      const spread = 30; // degrees spread across the fan
      return -spread / 2 + (spread / (total - 1)) * index;
  }
}
