import axios, { AxiosResponse } from 'axios';
import { IApiResponse } from '../types/account';
import { IAccount, IAccountCreateData, IAccountUpdateData, IStandardCategory, IStandardCategoryUpdateData } from '../types/account';
import { IFabricComponent, IFabricComponentCreateData, IFabricComponentUpdateData, ICategoryInfo } from '../types/fabric';

// 환경에 따라 API Base URL 설정
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000');

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
        try {
            const { accessToken } = JSON.parse(authData);
            if (accessToken) {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
        } catch (error) {
            console.error('API 요청 인터셉터 - authData 파싱 오류:', error);
        }
    }
    
    return config;
});

// 응답 인터셉터: 에러 처리
api.interceptors.response.use(
    (response: AxiosResponse) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            // 로그인 요청인지 확인
            const isLoginRequest = error.config?.url?.includes('/api/v1/auth/validate');
            
            // 로그인 요청이 아닌 경우에만 자동 리다이렉트
            if (!isLoginRequest) {
                localStorage.removeItem('auth');
                window.location.href = '/';
            }
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

    async post(url: string, data?: any, config?: any): Promise<IApiResponse<any>> {
        try {
            const response = await api.post(url, data, config);
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
    },

    async delete(url: string): Promise<IApiResponse<any>> {
        try {
            const response = await api.delete(url);
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

// accountApi를 apiWrapper를 사용하도록 수정
export const accountApi = {
  getAccounts: async (): Promise<IAccount[]> => {
    const response = await apiWrapper.get('/api/v1/accounts/');
    if (response.success && response.data) {
      return response.data.map(convertAccount);
    }
    throw new Error(response.message || 'Failed to fetch accounts');
  },

  getAccount: async (id: number): Promise<IAccount> => {
    const response = await apiWrapper.get(`/api/v1/accounts/${id}`);
    if (response.success && response.data) {
      return convertAccount(response.data);
    }
    throw new Error(response.message || 'Failed to fetch account');
  },

  createAccount: async (data: IAccountCreateData): Promise<IAccount> => {
    const response = await apiWrapper.post('/api/v1/accounts/', {
      name: data.name,
      code: data.code,
      role: data.role,
      isActive: data.isActive,
    });
    if (response.success && response.data) {
      return convertAccount(response.data);
    }
    throw new Error(response.message || 'Failed to create account');
  },

  updateAccount: async (id: number, data: IAccountUpdateData): Promise<IAccount> => {
    const response = await apiWrapper.put(`/api/v1/accounts/${id}`, {
      name: data.name,
      code: data.code,
      role: data.role,
      isActive: data.isActive,
    });
    if (response.success && response.data) {
      return convertAccount(response.data);
    }
    throw new Error(response.message || 'Failed to update account');
  },

  deleteAccount: async (id: number): Promise<void> => {
    const response = await apiWrapper.delete(`/api/v1/accounts/${id}`);
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete account');
    }
  },
};

// StandardCategory 관련 API
export const standardCategoryApi = {
    getCategories: async (): Promise<IStandardCategory[]> => {
        const response = await apiWrapper.get('/api/v1/categories/');
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to fetch categories');
    },

    updateCategory: async (id: number, data: IStandardCategoryUpdateData): Promise<IStandardCategory> => {
        const response = await apiWrapper.put(`/api/v1/categories/${id}`, data);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to update category');
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
        const response = await apiWrapper.get(url);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to fetch components');
    },

    getMajorCategories: async (): Promise<ICategoryInfo[]> => {
        const response = await apiWrapper.get('/api/v1/fabric-components/major-categories');
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to fetch major categories');
    },

    getMinorCategories: async (majorCategoryCode?: string): Promise<ICategoryInfo[]> => {
        const url = majorCategoryCode && majorCategoryCode !== 'all' 
            ? `/api/v1/fabric-components/minor-categories?major_category_code=${majorCategoryCode}`
            : '/api/v1/fabric-components/minor-categories';
        const response = await apiWrapper.get(url);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to fetch minor categories');
    },

    getComponent: async (id: number): Promise<IFabricComponent> => {
        const response = await apiWrapper.get(`/api/v1/fabric-components/${id}`);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to fetch component');
    },

    createComponent: async (data: IFabricComponentCreateData): Promise<IFabricComponent> => {
        const response = await apiWrapper.post('/api/v1/fabric-components/', data);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to create component');
    },

    updateComponent: async (id: number, data: IFabricComponentUpdateData): Promise<IFabricComponent> => {
        const response = await apiWrapper.put(`/api/v1/fabric-components/${id}`, data);
        if (response.success && response.data) {
            return response.data;
        }
        throw new Error(response.message || 'Failed to update component');
    },

    deleteComponent: async (id: number): Promise<void> => {
        const response = await apiWrapper.delete(`/api/v1/fabric-components/${id}`);
        if (!response.success) {
            throw new Error(response.message || 'Failed to delete component');
        }
    }
};

// HS Classification API
export const hsClassificationApi = {
  downloadTemplate: async () => {
    try {
      const response = await api.get('/api/v1/excel/hs-classification/template', {
        responseType: 'blob'
      });
      
      // 파일 다운로드
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'hs_code_template.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { success: true };
    } catch (error: any) {
      console.error('템플릿 다운로드 오류:', error);
      throw new Error('템플릿 다운로드에 실패했습니다');
    }
  },
  
  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiWrapper.post('/api/v1/excel/hs-classification/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
};

export default api; 