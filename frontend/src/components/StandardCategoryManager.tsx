import React, { useState, useEffect } from 'react';
import {
  Box,
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
  Button,
  Divider,
} from '@mui/material';
import { IStandardCategory, IStandardCategoryUpdateData } from '../types/account';
import { standardCategoryApi } from '../services/api';

const StandardCategoryManager: React.FC = () => {
  const [categories, setCategories] = useState<IStandardCategory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<IStandardCategory | null>(null);
  const [formData, setFormData] = useState<IStandardCategoryUpdateData>({
    category_name_ko: '',
    description: '',
    keywords: '',
  });

  const loadCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await standardCategoryApi.getCategories();
      setCategories(data);
    } catch (error) {
      setError('카테고리 목록을 불러오는데 실패했습니다.');
      console.error('카테고리 목록 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  const handleRowDoubleClick = (category: IStandardCategory) => {
    setSelectedCategory(category);
    setFormData({
      category_name_ko: category.category_name_ko || '',
      description: category.description || '',
      keywords: category.keywords || '',
    });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedCategory(null);
    setFormData({
      category_name_ko: '',
      description: '',
      keywords: '',
    });
    setError(null);
  };

  const handleSubmit = async () => {
    if (!selectedCategory) return;

    try {
      setLoading(true);
      setError(null);
      
      await standardCategoryApi.updateCategory(selectedCategory.id, formData);
      setSuccess('카테고리가 수정되었습니다.');
      
      handleCloseDialog();
      await loadCategories();
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || '카테고리 수정에 실패했습니다.';
      setError(errorMessage);
      console.error('카테고리 수정 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 3 }}>
        의류 카테고리 사전
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
          <CircularProgress />
        </Box>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell sx={{ fontWeight: 'bold' }}>카테고리 번호</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>카테고리 영문명</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>카테고리 한글명</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>설명</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>포함 단어</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {categories.map((category) => (
              <TableRow 
                key={category.id} 
                hover 
                sx={{ cursor: 'pointer' }}
                onDoubleClick={() => handleRowDoubleClick(category)}
              >
                <TableCell>{category.category_code}</TableCell>
                <TableCell>{category.category_name_en}</TableCell>
                <TableCell>{category.category_name_ko || '-'}</TableCell>
                <TableCell sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {category.description || '-'}
                </TableCell>
                <TableCell sx={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {category.keywords || '-'}
                </TableCell>
              </TableRow>
            ))}
            {categories.length === 0 && !loading && (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 3 }}>
                  카테고리 데이터가 없습니다.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* 수정 다이얼로그 */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle sx={{ 
          backgroundColor: '#f8f9fa', 
          borderBottom: '1px solid #e9ecef',
          fontWeight: 'bold',
          fontSize: '1.2rem'
        }}>
          카테고리 정보 수정
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          <Box sx={{ mt: 1 }}>
            {/* 카테고리 번호 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  카테고리 번호
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={selectedCategory?.category_code || ''}
                  disabled
                  variant="outlined"
                  size="small"
                  sx={{
                    '& .MuiInputBase-input.Mui-disabled': {
                      WebkitTextFillColor: '#6c757d',
                      backgroundColor: '#f8f9fa'
                    }
                  }}
                />
              </Box>
            </Box>

            {/* 카테고리 영문명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  카테고리 영문명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={selectedCategory?.category_name_en || ''}
                  disabled
                  variant="outlined"
                  size="small"
                  sx={{
                    '& .MuiInputBase-input.Mui-disabled': {
                      WebkitTextFillColor: '#6c757d',
                      backgroundColor: '#f8f9fa'
                    }
                  }}
                />
              </Box>
            </Box>

            {/* 카테고리 한글명 */}
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  카테고리 한글명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={formData.category_name_ko}
                  onChange={(e) => setFormData({ ...formData, category_name_ko: e.target.value })}
                  placeholder="한글명을 입력하세요"
                  variant="outlined"
                  size="small"
                />
              </Box>
            </Box>

            {/* 카테고리 설명 */}
            <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2, pt: 1 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  카테고리 설명
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="카테고리에 대한 설명을 입력하세요"
                  multiline
                  rows={3}
                  variant="outlined"
                  size="small"
                />
              </Box>
            </Box>

            {/* 포함 단어 */}
            <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
              <Box sx={{ width: '25%', pr: 2, pt: 1 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  포함 단어
                </Typography>
              </Box>
              <Box sx={{ width: '75%' }}>
                <TextField
                  fullWidth
                  value={formData.keywords}
                  onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                  placeholder="관련 키워드를 입력하세요"
                  multiline
                  rows={6}
                  variant="outlined"
                  size="small"
                />
              </Box>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 3, backgroundColor: '#f8f9fa', borderTop: '1px solid #e9ecef' }}>
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
            저장
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default StandardCategoryManager; 