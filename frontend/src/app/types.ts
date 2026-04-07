import z from "zod";
import { CardSchema } from "./types_spicy";

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
    roomCreated: z.object({
    type: z.literal('roomCreated'),
    roomId: z.string()
    }),
    join: z.object({
        type: z.literal('join'),
        roomId: z.string(),
        gameType: z.enum(['spicy', 'aow', 'space-pong', 'betrayal', 'wod'])
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
}

// For each entry in websocketMessageSchemaTypes, this builds a TypeScript type
// using the key as the message name and inferring the message's shape from the Zod schema.
// This prevents us from manually writing types and keeps schemas + types consistent.
export type WebSocketMessageTypes = {
    [K in keyof typeof websocketMessageSchemaTypes]: z.infer<typeof websocketMessageSchemaTypes[K]>
}