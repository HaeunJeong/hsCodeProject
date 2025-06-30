import React, { useState } from 'react';
import { Box, Button, Typography, Paper, Alert } from '@mui/material';
import { Upload as UploadIcon, Download as DownloadIcon, AutoFixHigh as MapIcon } from '@mui/icons-material';
import MappingRuleTable from './MappingRuleTable';
import { MappingRule } from '../types/mapping';
import { accessCodeApi } from '../services/api';
import * as XLSX from 'xlsx';

const MappingRuleManager: React.FC = () => {
    const [mappingRules, setMappingRules] = useState<MappingRule[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isMapping, setIsMapping] = useState(false);

    const handleTemplateDownload = () => {
        // 빈 데이터로 워크북 생성
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet([{
            styleNo: '',
            name: '',
            fabricType: '',
            category: '',
            gender: '',
            materialDetail: '',
            hsCode: '',
            note: ''
        }]);

        // 헤더 설정
        const headers = [
            ['StyleNo', 'Name', 'FabricType', 'Category', 'Gender', 'MaterialDetail', 'HSCode', 'Note'],
            ['제품번호', '제품명', 'knit / woven', '의류카테고리', 'men / women', '소재 함유 상세', '', '']
        ];
        XLSX.utils.sheet_add_aoa(ws, headers, { origin: 'A1' });

        // 워크북에 워크시트 추가
        XLSX.utils.book_append_sheet(wb, ws, 'Mapping Rules');

        // 엑셀 파일 다운로드
        XLSX.writeFile(wb, 'mapping_rules_template.xlsx');
    };

    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = new Uint8Array(e.target?.result as ArrayBuffer);
                const workbook = XLSX.read(data, { type: 'array' });
                const worksheet = workbook.Sheets[workbook.SheetNames[0]];
                
                // 데이터를 JSON으로 변환
                const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                
                // 헤더 검증
                const headers = jsonData.slice(0, 2);
                const expectedHeaders = [
                    ['StyleNo', 'Name', 'FabricType', 'Category', 'Gender', 'MaterialDetail', 'HSCode', 'Note'],
                    ['제품번호', '제품명', 'knit / woven', '의류카테고리', 'men / women', '소재 함유 상세', '', '']
                ];

                if (JSON.stringify(headers) !== JSON.stringify(expectedHeaders)) {
                    setError('템플릿 형식이 일치하지 않습니다.');
                    return;
                }

                // 데이터 변환
                const rules: MappingRule[] = jsonData.slice(2).map((row: any) => ({
                    styleNo: row[0] || '',
                    name: row[1] || '',
                    fabricType: row[2] || '',
                    category: row[3] || '',
                    gender: row[4] || '',
                    materialDetail: row[5] || '',
                    hsCode: row[6] || '',
                    note: row[7] || ''
                }));

                setMappingRules(rules);
                setError(null);
            } catch (error) {
                console.error('파일 처리 중 오류 발생:', error);
                setError('파일 처리 중 오류가 발생했습니다.');
            }
        };
        reader.readAsArrayBuffer(file);
    };

    const handleMapToHsCode = async () => {
        if (mappingRules.length === 0) {
            setError('매핑할 데이터가 없습니다.');
            return;
        }

        setIsMapping(true);
        try {
            // 빈 행 제거 (모든 필드가 비어있는 행)
            const validRules = mappingRules.filter(rule => 
                rule.styleNo || rule.name || rule.fabricType || 
                rule.category || rule.gender || rule.materialDetail
            );

            if (validRules.length === 0) {
                setError('유효한 데이터가 없습니다.');
                return;
            }

            const response = await accessCodeApi.post('/api/v1/mapping/map-to-hs-code', validRules);
            
            if (response.success && response.data) {
                setMappingRules(response.data);
                setError(null);
            } else {
                setError('HS코드 매핑에 실패했습니다.');
            }
        } catch (error: any) {
            console.error('HS코드 매핑 중 오류 발생:', error);
            setError(error.response?.data?.detail || 'HS코드 매핑 중 오류가 발생했습니다.');
        } finally {
            setIsMapping(false);
        }
    };

    const handleExport = () => {
        // 워크북 생성
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(mappingRules);

        // 헤더 설정
        const headers = [
            ['StyleNo', 'Name', 'FabricType', 'Category', 'Gender', 'MaterialDetail', 'HSCode', 'Note'],
            ['제품번호', '제품명', 'knit / woven', '의류카테고리', 'men / women', '소재 함유 상세', '', '']
        ];
        XLSX.utils.sheet_add_aoa(ws, headers, { origin: 'A1' });

        // 워크북에 워크시트 추가
        XLSX.utils.book_append_sheet(wb, ws, 'Mapping Rules');

        // 엑셀 파일 다운로드
        XLSX.writeFile(wb, 'mapping_rules_export.xlsx');
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
                HS 코드 매핑 관리
            </Typography>

            <Paper sx={{ p: 2, mb: 2 }}>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Button
                        variant="contained"
                        startIcon={<DownloadIcon />}
                        onClick={handleTemplateDownload}
                    >
                        템플릿 다운로드
                    </Button>
                    <Button
                        variant="contained"
                        component="label"
                        startIcon={<UploadIcon />}
                    >
                        엑셀 업로드
                        <input
                            type="file"
                            hidden
                            accept=".xlsx,.xls"
                            onChange={handleFileUpload}
                        />
                    </Button>
                    <Button
                        variant="contained"
                        color="secondary"
                        startIcon={<MapIcon />}
                        onClick={handleMapToHsCode}
                        disabled={mappingRules.length === 0 || isMapping}
                    >
                        {isMapping ? 'HS코드 매핑 중...' : 'HS코드 매핑'}
                    </Button>
                    <Button
                        variant="contained"
                        startIcon={<DownloadIcon />}
                        onClick={handleExport}
                        disabled={mappingRules.length === 0}
                    >
                        엑셀 다운로드
                    </Button>
                </Box>
            </Paper>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            <MappingRuleTable 
                data={mappingRules} 
                onDataChange={setMappingRules}
            />
        </Box>
    );
};

export default MappingRuleManager; 