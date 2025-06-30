export interface AuthState {
    isAuthenticated: boolean;
    accessCode: string | null;
    accessToken: string | null;
    role: string | null;
    error: string | null;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
} 