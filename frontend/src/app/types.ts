import z from "zod";

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
    })
}

// For each entry in websocketMessageSchemaTypes, this builds a TypeScript type
// using the key as the message name and inferring the message's shape from the Zod schema.
// This prevents us from manually writing types and keeps schemas + types consistent.
export type WebSocketMessageTypes = {
    [K in keyof typeof websocketMessageSchemaTypes]: z.infer<typeof websocketMessageSchemaTypes[K]>
}