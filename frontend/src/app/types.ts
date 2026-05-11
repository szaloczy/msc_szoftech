import z from "zod";
import { CardSchema, CardSuit } from "./types_spicy";

export interface GameMode {
    id: string;
    name: string;
    description: string;
    duration: string;
    player: number;
}

export interface User {
    id: string;
    name: string;
}

export interface UserApiResponse {
    success: boolean;
    data: User;
    error: string | null;
}

export const websocketMessageSchemaTypes = {
    auth: z.object({
        type: z.literal('auth'),
        success: z.boolean(),
        user_id: z.string().optional().nullable(),
        user_name: z.string().optional()
    }),
    lobbyCreated: z.object({
      type: z.literal('lobbyCreated'),
      room_id: z.string()
    }),
    join: z.object({
        type: z.literal('join'),
        room_id: z.string(),
        game_type: z.enum(['spicy'])
    }),
    roomData: z.object({
    type: z.literal('roomData'),
    currentTurn: z.string().nullable(),
    turns: z.array(z.string()),
    turnNames: z.array(z.string()),
    playerCards: z.record(z.string(), z.number()),
    currentLiedCard: CardSchema.nullable(),
    placedCardOwner: z.string().nullable(),
    yourCards: z.array(CardSchema),
    pileSize: z.number(),
    deckSize: z.number(),
    liarCaller: z.string().nullable(),
    plusTenCards: z.number(),
    playerReady: z.array(z.string()).nullable()
  }),
  placeCard: z.object({
    type: z.literal('placeCard'),
    roomId: z.string(),
    userId: z.string(),
    selectedCard: z.tuple([z.nativeEnum(CardSuit), z.number()]),
    liedCard: z.tuple([z.nativeEnum(CardSuit), z.number()])
  }),
  liarCalled: z.object({
    type: z.literal('liarCalled'),
    liarCaller: z.string()
  }),
  liarCalledFinished: z.object({
    type: z.literal('liarCalledFinished')
  }),
  newCards: z.object({
    type: z.literal('newCards'),
    allCards: z.array(CardSchema),
    newCards: z.array(CardSchema)
  }),
  turnChange: z.object({
    type: z.literal('turnChange'),
    currentTurn: z.string(),
    playerCards: z.record(z.string(), z.number()),
    currentLiedCard: CardSchema.nullable(),
    pileSize: z.number(),
    deckSize: z.number(),
    placedCardOwner: z.string().nullable(),
    liarCaller: z.string().nullable(),
    plusTenCards: z.number()
  }),
}

// For each entry in websocketMessageSchemaTypes, this builds a TypeScript type
// using the key as the message name and inferring the message's shape from the Zod schema.
// This prevents us from manually writing types and keeps schemas + types consistent.
export type WebSocketMessageTypes = {
    [K in keyof typeof websocketMessageSchemaTypes]: z.infer<typeof websocketMessageSchemaTypes[K]>
}
