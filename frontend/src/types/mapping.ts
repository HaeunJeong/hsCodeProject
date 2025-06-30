export interface IMappingRule {
    id: number;
    name: string;
    category: string;
    condition_field: string;
    condition_type: 'contains' | 'equals' | 'startswith';
    condition_value: string;
    hsCode: string;
    description?: string;
    priority: number;
    isActive: boolean;
}

export interface MappingRule {
    styleNo: string;
    name: string;
    fabricType: 'knit' | 'woven' | '';
    category: string;
    gender: 'men' | 'women' | '';
    materialDetail: string;
    hsCode: string;
    note: string;
}

export interface MappingRuleTableProps {
    data: MappingRule[];
    onDataChange: (data: MappingRule[]) => void;
} 