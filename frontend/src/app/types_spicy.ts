import { z } from 'zod';
import { websocketMessageSchemaTypes } from './types';

export enum CardSuit {
  Pepper = 'pepper',
  Chili = 'chili',
  Wasabi = 'wasabi'
}

export interface PlaceCardMessage {
  type: 'placeCard';
  roomId: string;
  selectedCard: SpicyCard;
  liedCard: SpicyCard;
}

export interface PlaceCardEvent {
  selected: SpicyCard;
  lied: SpicyCard;
  index: number;
}

export const CardSchema = z.tuple([z.nativeEnum(CardSuit), z.number()]);
export type SpicyCard = z.infer<typeof CardSchema>;

export const PlayerSchema = z.record(z.string(), z.number().min(0));

export type SpicyRoomData = z.infer<typeof websocketMessageSchemaTypes.roomData>;