import { Component, inject, OnInit } from '@angular/core';
import { SpicyService } from '../../services/spicy.service';
import { ActivatedRoute } from '@angular/router';
import { SpicyCard, SpicyRoomData } from '../../types_spicy';
import { OtherPlayerHand } from '../other-player-hand/other-player-hand';
import { UserCards } from '../user-cards/user-cards';
import { WebSocketService } from '../../services/web-socket.service';
import { CommonModule } from '@angular/common';
import { BaseComponent } from '../../shared/base-component/base-component';

@Component({
  selector: 'app-board',
  imports: [OtherPlayerHand, UserCards, CommonModule, OtherPlayerHand, UserCards],
  templateUrl: './board.html',
  styleUrl: './board.css',
})
export class Board extends BaseComponent implements OnInit {
  spicyService = inject(SpicyService);
  activatedRoute = inject(ActivatedRoute);

  roomData: SpicyRoomData | null = null;
  yourCards: SpicyCard[] = [];
  names: string[] = [];
  turnNames: string[] = [];
  card_numbers: number[] = [];
  remainingCards = 0;
  plusTenCards = 0;
  isLiarButtonDisabled = true;
  players: { name: string; card_number: number }[] = [];
  playerPositions: number[] = [];
  pileSize = 0;
  deckSize = 0;
  liedCardType?: string;
  currentTurn: string | null = null;
  isMyTurn = false;
  showLiarChoice = false;
  currentUser = localStorage.getItem('currentUser') || '';
  userId = '';
  isliarActive = false;
  liarCaller: string | null = null;
  placedCardOwner: string | null = null;

  leaderboardVisible = false;
  leaderboardData: string[] = [];

   ngOnInit() {
      this.webSocketService.subscribeToMessage('roomData', (message) => {
        this.roomData = message;
        this.remainingCards = message.deckSize;
        this.pileSize = message.pileSize;
        this.yourCards = this.roomData?.yourCards ?? [];
        this.plusTenCards = message.plusTenCards ?? 0;
        this.turnNames = message.turnNames;
        this.isMyTurn = message.currentTurn === this.userId;
        this.currentTurn = message.currentTurn;
        this.placedCardOwner = message.placedCardOwner ?? null;
        this.liarCaller = message.liarCaller ?? null;
        this.players = Object.entries(message.playerCards).map(([name, card_number]) => ({
          name,
          card_number
        }));

        this.playerPositions = getCustomArray(Object.keys(message.playerCards).length);
      }, this);
  }

  getPlayerCardsAtPosition(position: number): number {
    if (
      this.playerPositions[position] !== -1 &&
      this.players.length > 0 &&
      this.players[this.playerPositions[position]]
    ) {
      return this.players[this.playerPositions[position]].card_number;
    }
    return 0;
  }

  startGame() {
    const roomId = this.activatedRoute.snapshot.params['roomId'];
    const userId = JSON.parse(this.currentUser).id;

    console.log('Starting game with roomId:', roomId, 'and userId:', userId);

    this.spicyService.startGame(roomId, userId).subscribe();
  }


  lieCalled() {
    //TODO: Implement lie called logic
    return;
  }

  passTurn() {
    //TODO: Implement pass turn logic
    return;
  }

  getPlayerNameAtPosition(position: number): string {
    if (
      this.playerPositions[position] !== -1 &&
      this.players.length > 0 &&
      this.players[this.playerPositions[position]]
    ) {
      return this.turnNames[this.playerPositions[position]];
    }
    return '';
  }
}

function getCustomArray(length: number): number[] {

  switch (length) {
    case 1:
      return [-1, -1, 0, -1, -1];
    case 2:
      return [-1, 0, -1, 1, -1];
    case 3:
      return [0, -1, 1, -1, 2];
    case 4:
      return [0, 1, -1, 2, 3];
    case 5:
      return [0, 1, 2, 3, 4];
    default:
      return [];
  }
}
