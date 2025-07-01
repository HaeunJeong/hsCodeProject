import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Search as SearchIcon, Add as AddIcon } from '@mui/icons-material';
import { 
  IFabricComponent, 
  IFabricComponentCreateData, 
  IFabricComponentUpdateData, 
  ICategoryInfo,
  IFabricSearchFilters 
} from '../types/fabric';
import { fabricComponentApi } from '../services/api';

const initialFormData: IFabricComponentCreateData = {
  major_category_code: '',
  major_category_name: '',
  minor_category_code: '',
  minor_category_name: '',
  component_name_en: '',
  component_name_ko: '',
};

const FabricComponentManager: React.FC = () => {
  const [components, setComponents] = useState<IFabricComponent[]>([]);
  const [filteredComponents, setFilteredComponents] = useState<IFabricComponent[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState<IFabricComponentCreateData>(initialFormData);
  const [editingId, setEditingId] = useState<number | null>(null);
  
  // 카테고리 목록
  const [majorCategories, setMajorCategories] = useState<ICategoryInfo[]>([]);
  const [minorCategories, setMinorCategories] = useState<ICategoryInfo[]>([]);
  
  // 검색 필터
  const [searchFilters, setSearchFilters] = useState<IFabricSearchFilters>({
    major_category_code: 'all',
    minor_category_code: 'all',
    component_name_en: '',
    component_name_ko: ''
  });

  const loadComponents = async () => {
    try {
      setLoading(true);
      const data = await fabricComponentApi.getComponents();
      setComponents(data);
      setFilteredComponents(data);
    } catch (error) {
      setError('의류 성분 목록을 불러오는데 실패했습니다.');
      console.error('성분 목록 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMajorCategories = async () => {
    try {
      const data = await fabricComponentApi.getMajorCategories();
      setMajorCategories(data);
    } catch (error) {
      console.error('대분류 목록 로딩 실패:', error);
    }
  };

  const loadMinorCategories = async (majorCategoryCode?: string) => {
    try {
      const data = await fabricComponentApi.getMinorCategories(majorCategoryCode);
      setMinorCategories(data);
    } catch (error) {
      console.error('중분류 목록 로딩 실패:', error);
    }
  };

  useEffect(() => {
    loadComponents();
    loadMajorCategories();
    loadMinorCategories();
  }, []);

  // 대분류 변경 시 중분류 목록 업데이트
  useEffect(() => {
    loadMinorCategories(searchFilters.major_category_code);
    if (searchFilters.major_category_code !== 'all') {
      setSearchFilters(prev => ({ ...prev, minor_category_code: 'all' }));
    }
  }, [searchFilters.major_category_code]);

  const handleSearchFilterChange = (field: keyof IFabricSearchFilters, value: string) => {
    setSearchFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      
      const searchParams: any = {};
      
      if (searchFilters.major_category_code !== 'all') {
        searchParams.major_category_code = searchFilters.major_category_code;
      }
      if (searchFilters.minor_category_code !== 'all') {
        searchParams.minor_category_code = searchFilters.minor_category_code;
      }
      if (searchFilters.component_name_en.trim()) {
        searchParams.component_name_en = searchFilters.component_name_en.trim();
      }
      if (searchFilters.component_name_ko.trim()) {
        searchParams.component_name_ko = searchFilters.component_name_ko.trim();
      }
      
      const data = await fabricComponentApi.getComponents(searchParams);
      setFilteredComponents(data);
    } catch (error) {
      setError('검색 중 오류가 발생했습니다.');
      console.error('검색 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  // handleReset 함수 제거

  const handleOpenDialog = async (component?: IFabricComponent) => {
    if (component) {
      setFormData({
        major_category_code: component.major_category_code,
        major_category_name: component.major_category_name,
        minor_category_code: component.minor_category_code,
        minor_category_name: component.minor_category_name,
        component_name_en: component.component_name_en,
        component_name_ko: component.component_name_ko || '',
      });
      setEditingId(component.id);
      // 해당 대분류의 중분류 목록 로드
      await loadMinorCategories(component.major_category_code);
    } else {
      setFormData(initialFormData);
      setEditingId(null);
      // 신규 추가 시 중분류 목록 초기화
      setMinorCategories([]);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setFormData(initialFormData);
    setEditingId(null);
    setError(null);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // 필수 필드 검증
      if (!formData.major_category_code || !formData.minor_category_code || 
          !formData.component_name_en.trim()) {
        setError('모든 정보를 선택, 입력해야 저장할 수 있습니다.');
        return;
      }

      // 중복 검사 (신규 추가 또는 다른 항목으로 수정하는 경우)
      const isDuplicate = components.some(component => {
        // 수정 중인 항목은 제외
        if (editingId && component.id === editingId) return false;
        
        // 영문명 중복 검사
        if (component.component_name_en.toLowerCase() === formData.component_name_en.trim().toLowerCase()) {
          return true;
        }
        
        // 한글명 중복 검사 (한글명이 있는 경우에만)
        if (formData.component_name_ko && formData.component_name_ko.trim() && component.component_name_ko && 
            component.component_name_ko.toLowerCase() === formData.component_name_ko.trim().toLowerCase()) {
          return true;
        }
        
        return false;
      });

      if (isDuplicate) {
        // 어떤 필드가 중복인지 확인
        const duplicateEn = components.some(component => {
          if (editingId && component.id === editingId) return false;
          return component.component_name_en.toLowerCase() === formData.component_name_en.trim().toLowerCase();
        });
        
        const duplicateKo = formData.component_name_ko && formData.component_name_ko.trim() && components.some(component => {
          if (editingId && component.id === editingId) return false;
          return component.component_name_ko && 
                 component.component_name_ko.toLowerCase() === formData.component_name_ko!.trim().toLowerCase();
        });

        if (duplicateEn) {
          setError('이미 등록된 성분 영문명과 중복됩니다.');
        } else if (duplicateKo) {
          setError('이미 등록된 성분 한글명과 중복됩니다.');
        }
        return;
      }
      
      if (editingId) {
        await fabricComponentApi.updateComponent(editingId, formData);
        setSuccess('성분이 수정되었습니다.');
      } else {
        await fabricComponentApi.createComponent(formData);
        setSuccess('새 성분이 생성되었습니다.');
      }
      
      handleCloseDialog();
      await loadComponents();
      
      // 검색 조건이 있다면 다시 검색
      if (searchFilters.major_category_code !== 'all' || 
          searchFilters.minor_category_code !== 'all' ||
          searchFilters.component_name_en.trim() ||
          searchFilters.component_name_ko.trim()) {
        await handleSearch();
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || '저장에 실패했습니다.';
      setError(errorMessage);
      console.error('저장 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('정말 삭제하시겠습니까?')) return;
    
    try {
      setLoading(true);
      await fabricComponentApi.deleteComponent(id);
      setSuccess('성분이 삭제되었습니다.');
      await loadComponents();
      setOpenDialog(false); // 다이얼로그 닫기
      
      // 검색 조건이 있다면 다시 검색
      if (searchFilters.major_category_code !== 'all' || 
          searchFilters.minor_category_code !== 'all' ||
          searchFilters.component_name_en.trim() ||
          searchFilters.component_name_ko.trim()) {
        await handleSearch();
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || '삭제에 실패했습니다.';
      setError(errorMessage);
      console.error('삭제 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 3 }}>
        의류 성분 사전
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* 검색 필터 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end', flexWrap: 'wrap' }}>
          {/* 대분류명 */}
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>대분류명</InputLabel>
            <Select
              value={searchFilters.major_category_code}
              label="대분류명"
              onChange={(e) => handleSearchFilterChange('major_category_code', e.target.value)}
              size="small"
            >
              <MenuItem value="all">전체</MenuItem>
              {majorCategories.map((category) => (
                <MenuItem key={category.code} value={category.code}>
                  {category.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* 중분류명 */}
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>중분류명</InputLabel>
            <Select
              value={searchFilters.minor_category_code}
              label="중분류명"
              onChange={(e) => handleSearchFilterChange('minor_category_code', e.target.value)}
              size="small"
            >
              <MenuItem value="all">전체</MenuItem>
              {minorCategories.map((category) => (
                <MenuItem key={category.code} value={category.code}>
                  {category.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* 성분 영문명 */}
          <TextField
            label="성분 영문명"
            value={searchFilters.component_name_en}
            onChange={(e) => handleSearchFilterChange('component_name_en', e.target.value)}
            size="small"
            sx={{ minWidth: 150 }}
          />

          {/* 성분 한글명 */}
          <TextField
            label="성분 한글명"
            value={searchFilters.component_name_ko}
            onChange={(e) => handleSearchFilterChange('component_name_ko', e.target.value)}
            size="small"
            sx={{ minWidth: 150 }}
          />

                     {/* 버튼들 */}
           <Box sx={{ display: 'flex', gap: 1 }}>
             <Button
               variant="contained"
               startIcon={<SearchIcon />}
               onClick={handleSearch}
               disabled={loading}
             >
               검색
             </Button>
             <Button
               variant="outlined"
               startIcon={<AddIcon />}
               onClick={() => handleOpenDialog()}
               sx={{ 
                 backgroundColor: 'white',
                 color: '#666',
                 borderColor: '#ddd',
                 '&:hover': {
                   backgroundColor: '#f8f9fa',
                   borderColor: '#ccc'
                 }
               }}
             >
               추가하기
             </Button>
           </Box>
        </Box>
      </Paper>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
          <CircularProgress />
        </Box>
      )}

      {/* 성분 목록 테이블 */}
      <TableContainer component={Paper}>
        <Table>
                     <TableHead>
             <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
               <TableCell sx={{ fontWeight: 'bold' }}>대분류명</TableCell>
               <TableCell sx={{ fontWeight: 'bold' }}>중분류명</TableCell>
               <TableCell sx={{ fontWeight: 'bold' }}>성분 영문명</TableCell>
               <TableCell sx={{ fontWeight: 'bold' }}>성분 한글명</TableCell>
             </TableRow>
           </TableHead>
          <TableBody>
                         {filteredComponents.map((component) => (
               <TableRow 
                 key={component.id} 
                 hover 
                 sx={{ cursor: 'pointer' }}
                 onClick={() => handleOpenDialog(component)}
               >
                 <TableCell>{component.major_category_name}</TableCell>
                 <TableCell>{component.minor_category_name}</TableCell>
                 <TableCell>{component.component_name_en}</TableCell>
                 <TableCell>{component.component_name_ko || '-'}</TableCell>
               </TableRow>
             ))}
                         {filteredComponents.length === 0 && !loading && (
               <TableRow>
                 <TableCell colSpan={4} align="center" sx={{ py: 3 }}>
                   성분 데이터가 없습니다.
                 </TableCell>
               </TableRow>
             )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* 수정/추가 다이얼로그 */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle sx={{ 
          backgroundColor: '#f8f9fa', 
          borderBottom: '1px solid #e9ecef',
          fontWeight: 'bold',
          fontSize: '1.2rem'
        }}>
          {editingId ? '의류 성분 수정' : '의류 성분 신규 추가'}
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Box sx={{ mt: 1 }}>
            {/* 성분 대분류명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  성분 대분류명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <FormControl fullWidth required size="small">
                  <Select
                    value={formData.major_category_code}
                    onChange={async (e) => {
                      const selectedCode = e.target.value;
                      const selectedCategory = majorCategories.find(cat => cat.code === selectedCode);
                      setFormData({ 
                        ...formData, 
                        major_category_code: selectedCode,
                        major_category_name: selectedCategory?.name || '',
                        minor_category_code: '',
                        minor_category_name: ''
                      });
                      // 중분류 목록 업데이트
                      await loadMinorCategories(selectedCode);
                    }}
                    displayEmpty
                    variant="outlined"
                  >
                    {!formData.major_category_code && (
                      <MenuItem value="" disabled>
                        대분류를 선택하세요
                      </MenuItem>
                    )}
                    {majorCategories.map((category) => (
                      <MenuItem key={category.code} value={category.code}>
                        {category.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>

            {/* 성분 중분류명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  성분 중분류명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <FormControl fullWidth required size="small">
                  <Select
                    value={formData.minor_category_code}
                    onChange={(e) => {
                      const selectedCode = e.target.value;
                      const selectedCategory = minorCategories.find(cat => cat.code === selectedCode);
                      setFormData({ 
                        ...formData, 
                        minor_category_code: selectedCode,
                        minor_category_name: selectedCategory?.name || ''
                      });
                    }}
                    disabled={!formData.major_category_code}
                    displayEmpty
                    variant="outlined"
                  >
                    {!formData.minor_category_code && (
                      <MenuItem value="" disabled>
                        {!formData.major_category_code ? '대분류를 먼저 선택하세요' : '중분류를 선택하세요'}
                      </MenuItem>
                    )}
                    {minorCategories.map((category) => (
                      <MenuItem key={category.code} value={category.code}>
                        {category.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>

            {/* 성분 영문명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  성분 영문명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={formData.component_name_en}
                  onChange={(e) => setFormData({ ...formData, component_name_en: e.target.value })}
                  placeholder="modal"
                  variant="outlined"
                  size="small"
                  required
                />
              </Box>
            </Box>

            {/* 성분 한글명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  성분 한글명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={formData.component_name_ko}
                  onChange={(e) => setFormData({ ...formData, component_name_ko: e.target.value })}
                  placeholder="모달"
                  variant="outlined"
                  size="small"
                />
              </Box>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 3, backgroundColor: '#f8f9fa', borderTop: '1px solid #e9ecef' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
            <Box>
              {editingId && (
                <Button 
                  onClick={() => handleDelete(editingId)} 
                  variant="outlined"
                  color="error"
                  disabled={loading}
                  sx={{ 
                    minWidth: 80,
                    '&:hover': {
                      backgroundColor: 'rgba(211, 47, 47, 0.04)'
                    }
                  }}
                >
                  삭제
                </Button>
              )}
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button 
                onClick={handleCloseDialog}
                variant="outlined"
                sx={{ 
                  minWidth: 80,
                  color: '#6c757d',
                  borderColor: '#6c757d',
                  '&:hover': {
                    borderColor: '#5a6268',
                    backgroundColor: 'rgba(108, 117, 125, 0.04)'
                  }
                }}
              >
                취소
              </Button>
              <Button 
                onClick={handleSubmit} 
                variant="contained"
                disabled={loading}
                sx={{ 
                  minWidth: 80,
                  backgroundColor: '#007bff',
                  '&:hover': {
                    backgroundColor: '#0056b3'
                  }
                }}
              >
                {editingId ? '수정' : '저장'}
              </Button>
            </Box>
          </Box>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FabricComponentManager; 