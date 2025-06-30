import axios, { AxiosResponse } from 'axios';
import { IProduct } from '../types/product';
import { IApiResponse } from '../types/account';
import { IMappingRule } from '../types/mapping';
import { IExcelData } from '../types/excel';
import { IAccount, IAccountCreateData, IAccountUpdateData, IStandardCategory, IStandardCategoryUpdateData } from '../types/account';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 요청 인터셉터: 토큰 자동 추가
api.interceptors.request.use((config) => {
    const authData = localStorage.getItem('auth');
    if (authData) {
        const { accessToken } = JSON.parse(authData);
        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
    }
    return config;
});

// 응답 인터셉터: 에러 처리
api.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('auth');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// 엑셀 파일 업로드
export const uploadExcelFile = async (file: File): Promise<IApiResponse<IProduct[]>> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<IApiResponse<IProduct[]>>('/excel/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// 매핑 룰 관련 API
export const mappingRuleApi = {
    getRules: async (category?: string): Promise<IApiResponse<IMappingRule[]>> => {
        const response = await api.get<IApiResponse<IMappingRule[]>>('/mapping-rules', {
            params: { category },
        });
        return response.data;
    },

    createRule: async (rule: Omit<IMappingRule, 'id'>): Promise<IApiResponse<IMappingRule>> => {
        const response = await api.post<IApiResponse<IMappingRule>>('/mapping-rules', rule);
        return response.data;
    },

    updateRule: async (id: number, rule: Partial<IMappingRule>): Promise<IApiResponse<IMappingRule>> => {
        const response = await api.put<IApiResponse<IMappingRule>>(`/mapping-rules/${id}`, rule);
        return response.data;
    },

    deleteRule: async (id: number): Promise<IApiResponse<void>> => {
        const response = await api.delete<IApiResponse<void>>(`/mapping-rules/${id}`);
        return response.data;
    },

    uploadExcel: async (formData: FormData): Promise<IApiResponse<IExcelData[]>> => {
        const response = await api.post('/excel/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    exportExcel: async (data: IExcelData[]): Promise<Blob> => {
        const response = await api.post('/excel/export', data, {
            responseType: 'blob',
        });
        return response.data;
    },

    downloadTemplate: async (): Promise<Blob> => {
        const response = await api.get('/excel/template', {
            responseType: 'blob',
        });
        return response.data;
    },

    mapHsCodes: async (data: IExcelData[]): Promise<IApiResponse<IExcelData[]>> => {
        const response = await api.post<IApiResponse<IExcelData[]>>('/excel/map-hs-codes', data);
        return response.data;
    },
};

// API 래퍼 함수들
const apiWrapper = {
    async get(url: string): Promise<IApiResponse<any>> {
        try {
            const response = await api.get(url);
            // 백엔드가 이미 {success, data} 형태로 응답하는 경우 그대로 반환
            if (response.data && typeof response.data === 'object' && 'success' in response.data) {
                return response.data;
            }
            // 기존 형태의 응답인 경우 (배열이나 객체 직접 반환)
            return {
                success: true,
                data: response.data,
                message: response.statusText
            };
        } catch (error: any) {
            return {
                success: false,
                data: null,
                message: error.response?.data?.detail || error.message
            };
        }
    },

    async post(url: string, data?: any): Promise<IApiResponse<any>> {
        try {
            const response = await api.post(url, data);
            // 백엔드가 이미 {success, data} 형태로 응답하므로 그대로 반환
            if (response.data && typeof response.data === 'object' && 'success' in response.data) {
                return response.data;
            }
            // 기존 형태의 응답인 경우
            return {
                success: true,
                data: response.data,
                message: response.statusText
            };
        } catch (error: any) {
            return {
                success: false,
                data: null,
                message: error.response?.data?.detail || error.message
            };
        }
    },

    async put(url: string, data?: any): Promise<IApiResponse<any>> {
        try {
            const response = await api.put(url, data);
            // 백엔드가 이미 {success, data} 형태로 응답하는 경우 그대로 반환
            if (response.data && typeof response.data === 'object' && 'success' in response.data) {
                return response.data;
            }
            // 기존 형태의 응답인 경우
            return {
                success: true,
                data: response.data,
                message: response.statusText
            };
        } catch (error: any) {
            return {
                success: false,
                data: null,
                message: error.response?.data?.detail || error.message
            };
        }
    }
};

// 접속 코드 관련 API
export const accessCodeApi = {
    validate: async (code: string): Promise<IApiResponse<{
        accessCode: string;
        role: string;
        access_token: string;
        token_type: string;
        expiresAt?: string;
    }>> => {
        return await apiWrapper.post('/api/v1/auth/validate', { code });
    },

    deactivate: async (code: string): Promise<IApiResponse<void>> => {
        return await apiWrapper.post('/api/v1/auth/deactivate', { code });
    },

    getAll: async (): Promise<IApiResponse<any[]>> => {
        return await apiWrapper.get('/api/v1/accounts/');
    },

    create: async (data: { 
        code: string; 
        role: string; 
        expiresAt?: string; 
    }): Promise<IApiResponse<any>> => {
        return await apiWrapper.post('/api/v1/auth/codes', data);
    },

    // 매핑 관련 API 추가
    post: async (url: string, data: any): Promise<IApiResponse<any>> => {
        return await apiWrapper.post(url, data);
    },

    get: async (url: string): Promise<IApiResponse<any>> => {
        return await apiWrapper.get(url);
    }
};

const convertAccount = (account: any): IAccount => ({
  id: account.id,
  name: account.name,
  code: account.code,
  role: account.role,
  isActive: account.isActive,
  createdAt: account.createdAt,
  updatedAt: account.updatedAt,
});

export const accountApi = {
  getAccounts: async (): Promise<IAccount[]> => {
    const response = await api.get<any[]>('/api/v1/accounts/');
    return response.data.map(convertAccount);
  },

  getAccount: async (id: number): Promise<IAccount> => {
    const response = await api.get<any>(`/api/v1/accounts/${id}`);
    return convertAccount(response.data);
  },

  createAccount: async (data: IAccountCreateData): Promise<IAccount> => {
    const response = await api.post<any>('/api/v1/accounts/', {
      name: data.name,
      code: data.code,
      role: data.role,
      isActive: data.isActive,
    });
    return convertAccount(response.data);
  },

  updateAccount: async (id: number, data: IAccountUpdateData): Promise<IAccount> => {
    const response = await api.put<any>(`/api/v1/accounts/${id}`, {
      name: data.name,
      code: data.code,
      role: data.role,
      isActive: data.isActive,
    });
    return convertAccount(response.data);
  },

  deleteAccount: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/accounts/${id}`);
  },
};

export const templateApi = {
  async download() {
    const response = await fetch('/api/templates/download');
    if (!response.ok) {
      throw new Error('템플릿 다운로드에 실패했습니다.');
    }
    return response;
  },

  async upload(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/templates/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('템플릿 업로드에 실패했습니다.');
    }

    return response.json();
  },
};

// StandardCategory 관련 API
export const standardCategoryApi = {
    getCategories: async (): Promise<IStandardCategory[]> => {
        const response = await api.get<IStandardCategory[]>('/api/v1/categories/');
        return response.data;
    },

    updateCategory: async (id: number, data: IStandardCategoryUpdateData): Promise<IStandardCategory> => {
        const response = await api.put<IStandardCategory>(`/api/v1/categories/${id}`, data);
        return response.data;
    }
};

export default api; 