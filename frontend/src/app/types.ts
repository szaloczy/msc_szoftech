export interface GameMode {
    id: string;
    name: string;
    description: string;
    duration: string;
    player: number;
}

export interface User {
    id: string;
    username: string;
}

export interface UserApiResponse {
    success: boolean;
    data: User;
    error: string | null;
}
