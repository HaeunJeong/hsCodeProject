import axios, { AxiosResponse } from 'axios';
import { IApiResponse } from '../types/account';
import { IAccount, IAccountCreateData, IAccountUpdateData, IStandardCategory, IStandardCategoryUpdateData } from '../types/account';
import { IFabricComponent, IFabricComponentCreateData, IFabricComponentUpdateData, ICategoryInfo } from '../types/fabric';

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

// FabricComponent 관련 API
export const fabricComponentApi = {
    getComponents: async (params?: {
        major_category_code?: string;
        minor_category_code?: string;
        component_name_en?: string;
        component_name_ko?: string;
    }): Promise<IFabricComponent[]> => {
        const queryParams = new URLSearchParams();
        if (params?.major_category_code && params.major_category_code !== 'all') {
            queryParams.append('major_category_code', params.major_category_code);
        }
        if (params?.minor_category_code && params.minor_category_code !== 'all') {
            queryParams.append('minor_category_code', params.minor_category_code);
        }
        if (params?.component_name_en) {
            queryParams.append('component_name_en', params.component_name_en);
        }
        if (params?.component_name_ko) {
            queryParams.append('component_name_ko', params.component_name_ko);
        }
        
        const url = `/api/v1/fabric-components/${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
        const response = await api.get<IFabricComponent[]>(url);
        return response.data;
    },

    getMajorCategories: async (): Promise<ICategoryInfo[]> => {
        const response = await api.get<ICategoryInfo[]>('/api/v1/fabric-components/major-categories');
        return response.data;
    },

    getMinorCategories: async (majorCategoryCode?: string): Promise<ICategoryInfo[]> => {
        const url = majorCategoryCode && majorCategoryCode !== 'all' 
            ? `/api/v1/fabric-components/minor-categories?major_category_code=${majorCategoryCode}`
            : '/api/v1/fabric-components/minor-categories';
        const response = await api.get<ICategoryInfo[]>(url);
        return response.data;
    },

    getComponent: async (id: number): Promise<IFabricComponent> => {
        const response = await api.get<IFabricComponent>(`/api/v1/fabric-components/${id}`);
        return response.data;
    },

    createComponent: async (data: IFabricComponentCreateData): Promise<IFabricComponent> => {
        const response = await api.post<IFabricComponent>('/api/v1/fabric-components/', data);
        return response.data;
    },

    updateComponent: async (id: number, data: IFabricComponentUpdateData): Promise<IFabricComponent> => {
        const response = await api.put<IFabricComponent>(`/api/v1/fabric-components/${id}`, data);
        return response.data;
    },

    deleteComponent: async (id: number): Promise<void> => {
        await api.delete(`/api/v1/fabric-components/${id}`);
    }
};

export default api; 