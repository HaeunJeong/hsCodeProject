export interface IAccount {
    id: number;
    name: string;      // 고객사명
    code: string;      // 계정코드
    role: string;      // "admin" 또는 "client"
    isActive: boolean; // 사용여부
    createdAt: string;
    updatedAt: string | null;
}

export interface IAccountCreateData {
    name: string;
    code: string;      // 수동 입력
    role: string;      // "admin" 또는 "client"
    isActive: boolean;
}

export interface IAccountUpdateData {
    name?: string;
    code?: string;
    role?: string;
    isActive?: boolean;
}

export interface IAccountFormData {
    name: string;
    code: string;
    role: string;
    isActive: boolean;
} 

export interface IApiResponse<T> {
    success: boolean;
    data: T;
    message?: string;
}

// StandardCategory 타입 추가
export interface IStandardCategory {
    id: number;
    category_code: string;      // 카테고리 번호 (CAT001 등)
    category_name_en: string;   // 카테고리 영문명
    category_name_ko?: string;  // 카테고리 한글명
    description?: string;       // 설명
    keywords?: string;          // 포함 단어
}

export interface IStandardCategoryUpdateData {
    category_name_ko?: string;
    description?: string;
    keywords?: string;
} 