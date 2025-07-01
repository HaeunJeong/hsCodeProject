export interface IFabricComponent {
    id: number;
    major_category_code: string;    // 대분류 코드
    major_category_name: string;    // 대분류명
    minor_category_code: string;    // 중분류 코드
    minor_category_name: string;    // 중분류명
    component_name_en: string;      // 성분 영문명
    component_name_ko?: string;     // 성분 한글명
    created_at: string;
    updated_at?: string;
}

export interface IFabricComponentCreateData {
    major_category_code: string;
    major_category_name: string;
    minor_category_code: string;
    minor_category_name: string;
    component_name_en: string;
    component_name_ko?: string;
}

export interface IFabricComponentUpdateData {
    major_category_code?: string;
    major_category_name?: string;
    minor_category_code?: string;
    minor_category_name?: string;
    component_name_en?: string;
    component_name_ko?: string;
}

export interface ICategoryInfo {
    code: string;
    name: string;
}

export interface IFabricSearchFilters {
    major_category_code: string;    // 대분류 코드
    minor_category_code: string;    // 중분류 코드
    component_name_en: string;      // 성분 영문명
    component_name_ko: string;      // 성분 한글명
} 