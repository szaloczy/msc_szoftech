import { Component, Input } from '@angular/core';
import { CardSuit, PlaceCardEvent, SpicyCard } from '../../types_spicy';
import { Card } from "../card/card";

@Component({
  selector: 'app-user-cards',
  imports: [Card],
  templateUrl: './user-cards.html',
  styleUrl: './user-cards.css',
})
export class UserCards {
  @Input() defaultDeclaredSuit:CardSuit = CardSuit.Pepper;
  @Input() defaultDeclaredValue = 1;
  @Input() disabled = false;

  @Input() cards: SpicyCard[] = [];

  selectedCardIndex: number | null = null;
  selectedDeclaredSuit: CardSuit = this.defaultDeclaredSuit;
  selectedDeclaredValue: number = this.defaultDeclaredValue;

  onCardSelect(index: number) {
    this.selectedCardIndex = index;
  }

  onPlaceCard(event: PlaceCardEvent) {
    // Should be replaced with actual logic via websocket to handle the card placement
    this.cards.splice(event.index, 1);

    if (this.selectedCardIndex === event.index) {
      this.selectedCardIndex = null;
    }
  }

  onDeclaredChange(event: { suit: string; value: number }) {
    this.selectedDeclaredSuit = event.suit as CardSuit;
    this.selectedDeclaredValue = event.value;
  }
}
