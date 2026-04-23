import { Component, EventEmitter, inject, Input, Output } from '@angular/core';
import { CardSuit, PlaceCardEvent, PlaceCardMessage, SpicyCard } from '../../types_spicy';
import { WebSocketService } from '../../services/web-socket.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-card',
  imports: [CommonModule, FormsModule],
  templateUrl: './card.html',
  styleUrl: './card.css',
})
export class Card {
  webSocketService = inject(WebSocketService);
  activatedRoute = inject(ActivatedRoute);

  @Input({ required: true }) value!: number;
  @Input({ required: true }) suit!: CardSuit;
  @Input() isSelected = false;
  @Input() disabled = false;

  @Input() declaredSuit!: string;
  @Input() declaredValue!: number;

  @Input() cardIndex!: number;

  @Output() placeCard = new EventEmitter<PlaceCardEvent>();
  @Output() declaredChange = new EventEmitter<{ suit: string; value: number }>();

  cardImageUrl = '';

  get cardColor(): string {
    switch (this.suit) {
      case CardSuit.Pepper: return 'blue';
      case CardSuit.Chili: return 'red';
      case CardSuit.Wasabi: return 'green';
      default: return 'gray';
    }
  }

  emitDeclaredChange() {
    this.declaredChange.emit({
      suit: this.declaredSuit,
      value: this.declaredValue
    });
  }

  submitCard(event: Event) {
    event.preventDefault();

    const selectedCard: SpicyCard = [this.suit, this.value];
    const liedCard: SpicyCard = [this.declaredSuit as CardSuit, this.declaredValue];

    const message: PlaceCardMessage = {
      type: 'placeCard',
      roomId: this.activatedRoute.snapshot.params['roomId'],
      selectedCard,
      liedCard
    };
    this.webSocketService.sendMessage(message);

    this.placeCard.emit({
      selected: selectedCard,
      lied: liedCard,
      index: this.cardIndex
    });
  }
}
