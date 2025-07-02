import React, { useState, useRef } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Assignment as AssignmentIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  UnfoldMore as UnfoldMoreIcon,
  Edit as EditIcon,
  Check as CheckIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { hsClassificationApi } from '../services/api';
import * as XLSX from 'xlsx';

// 정렬 방향 타입 정의
type SortDirection = 'asc' | 'desc';

// 테이블 데이터 타입 정의
interface TableRow {
  style_no: string;
  product_name: string;
  weaving_type: string;
  category: string;
  gender: string;
  composition: string;
  hs_code: string;
  note: string;
  isModified?: boolean;
}

const HSClassification: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [downloadingTemplate, setDownloadingTemplate] = useState(false);

  const [alert, setAlert] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [showUploadArea, setShowUploadArea] = useState(true);
  const [showResults, setShowResults] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // 정렬 관련 상태
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [tableData, setTableData] = useState<TableRow[]>([]);

  // 편집 관련 상태
  const [editingCell, setEditingCell] = useState<{ rowIndex: number; value: string } | null>(null);
  const [originalValue, setOriginalValue] = useState<string>('');
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editedValue, setEditedValue] = useState<string>('');

  // 양식 다운로드
  const handleDownloadTemplate = async () => {
    setDownloadingTemplate(true);
    setAlert(null);
    
    try {
      await hsClassificationApi.downloadTemplate();
      setAlert({ type: 'success', message: '양식 다운로드가 완료되었습니다.' });
    } catch (error) {
      setAlert({ type: 'error', message: '양식 다운로드 중 오류가 발생했습니다.' });
    } finally {
      setDownloadingTemplate(false);
    }
  };

  // 정렬 핸들러
  const handleSort = (column: string) => {
    let newDirection: SortDirection = 'asc';
    
    if (sortColumn === column) {
      newDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    }
    
    setSortColumn(column);
    setSortDirection(newDirection);
    
    // 테이블 데이터 정렬 (isModified 상태 유지)
    const sortedData = [...tableData].sort((a, b) => {
      const aValue = String(a[column as keyof TableRow] || '');
      const bValue = String(b[column as keyof TableRow] || '');
      
      if (aValue < bValue) return newDirection === 'asc' ? -1 : 1;
      if (aValue > bValue) return newDirection === 'asc' ? 1 : -1;
      return 0;
    });
    
    setTableData(sortedData);
  };

  // 정렬 아이콘 렌더링
  const renderSortIcon = (column: string) => {
    if (sortColumn !== column) {
      return <UnfoldMoreIcon sx={{ fontSize: 16, ml: 0.5, color: '#999' }} />;
    }
    
    return sortDirection === 'asc' ? 
      <ArrowUpwardIcon sx={{ fontSize: 16, ml: 0.5 }} /> : 
      <ArrowDownwardIcon sx={{ fontSize: 16, ml: 0.5 }} />;
  };

  // HS Code 더블클릭 핸들러
  const handleHSCodeDoubleClick = (rowIndex: number, currentValue: string) => {
    setEditingCell({ rowIndex, value: currentValue });
    setOriginalValue(currentValue);
    setEditedValue(currentValue);
    setEditDialogOpen(true);
  };

  // 편집 확인 핸들러
  const handleEditConfirm = () => {
    if (editingCell) {
      const newTableData = [...tableData];
      newTableData[editingCell.rowIndex] = {
        ...newTableData[editingCell.rowIndex],
        hs_code: editedValue,
        isModified: editedValue !== originalValue
      };
      setTableData(newTableData);
    }
    
    setEditDialogOpen(false);
    setEditingCell(null);
    setOriginalValue('');
    setEditedValue('');
  };

  // 편집 취소 핸들러
  const handleEditCancel = () => {
    setEditDialogOpen(false);
    setEditingCell(null);
    setOriginalValue('');
    setEditedValue('');
  };

  // 파일 선택 처리
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
        setSelectedFile(file);
        setAlert(null);
        setUploadResult(null);
      } else {
        setAlert({ type: 'error', message: 'Excel 파일만 업로드 가능합니다.' });
        event.target.value = '';
      }
    }
  };

  // 드래그 앤 드롭 처리
  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
        setSelectedFile(file);
        setAlert(null);
        setUploadResult(null);
      } else {
        setAlert({ type: 'error', message: 'Excel 파일만 업로드 가능합니다.' });
      }
    }
  };

  // 파일 업로드 영역 클릭
  const handleUploadAreaClick = () => {
    fileInputRef.current?.click();
  };

  // HS코드 분류 처리
  const handleClassification = async () => {
    if (!selectedFile) {
      setAlert({ type: 'error', message: '파일을 선택해주세요.' });
      return;
    }

    setUploading(true);
    setAlert(null);
    setUploadResult(null);

    try {
      const response = await hsClassificationApi.uploadFile(selectedFile);
      
      if (response.success) {
        setUploadResult(response.data);
        // 테이블 데이터 초기화
        setTableData(response.data.results.map((item: any) => ({
          ...item,
          isModified: false
        })));
        setSortColumn(null);
        setSortDirection('asc');
        setShowUploadArea(false);
        setShowResults(true);
      } else {
        setAlert({ type: 'error', message: response.message || 'HS코드 분류 중 오류가 발생했습니다.' });
      }
    } catch (error) {
      setAlert({ type: 'error', message: 'HS코드 분류 중 오류가 발생했습니다.' });
    } finally {
      setUploading(false);
    }
  };

  const handleDownloadResult = async () => {
    if (!tableData || tableData.length === 0) {
      setAlert({ type: 'error', message: '다운로드할 데이터가 없습니다.' });
      return;
    }

    setAlert(null);

    try {
      // 엑셀 데이터 준비
      const excelData = tableData.map((row, index) => ({
        '수정여부': row.isModified ? '수정됨' : '',
        'Style No': row.style_no,
        '이름': row.product_name,
        '소재타입': row.weaving_type,
        '카테고리': row.category,
        '성별': row.gender,
        '상세 성분': row.composition,
        'HS Code': row.hs_code,
        'Note': row.note
      }));

      // 워크북 생성
      const workbook = XLSX.utils.book_new();
      const worksheet = XLSX.utils.json_to_sheet(excelData);

      // 컬럼 너비 설정
      const columnWidths = [
        { wch: 10 }, // 수정여부
        { wch: 15 }, // Style No
        { wch: 20 }, // 이름
        { wch: 12 }, // 소재타입
        { wch: 15 }, // 카테고리
        { wch: 8 },  // 성별
        { wch: 30 }, // 상세 성분
        { wch: 12 }, // HS Code
        { wch: 20 }  // Note
      ];
      worksheet['!cols'] = columnWidths;

      // 워크시트를 워크북에 추가
      XLSX.utils.book_append_sheet(workbook, worksheet, 'HS코드 분류 결과');

      // 파일명 생성 (현재 날짜/시간 포함)
      const now = new Date();
      const dateStr = now.toISOString().slice(0, 19).replace(/:/g, '-');
      const filename = `HS코드_분류결과_${uploadResult?.filename || 'unknown'}_${dateStr}.xlsx`;

      // 파일 다운로드
      XLSX.writeFile(workbook, filename);

      setAlert({ type: 'success', message: '엑셀 파일 다운로드가 완료되었습니다.' });
    } catch (error) {
      console.error('Excel download error:', error);
      setAlert({ type: 'error', message: '엑셀 다운로드 중 오류가 발생했습니다.' });
    }
  };

  // 다른 파일로 다시 시작하기
  const handleStartOver = () => {
    setShowResults(false);
    setShowUploadArea(true);
    setSelectedFile(null);
    setUploadResult(null);
    setAlert(null);
    setTableData([]);
    setSortColumn(null);
    setSortDirection('asc');
    // 파일 입력 초기화
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <Box sx={{ padding: 3 }}>

      {alert && (
        <Alert severity={alert.type} sx={{ marginBottom: 3 }}>
          {alert.message}
        </Alert>
      )}

      {/* 파일 업로드 영역 */}
      {showUploadArea && (
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ marginBottom: 2, display: 'flex', alignItems: 'center' }}>
              <AssignmentIcon sx={{ marginRight: 1 }} />
              파일 업로드
            </Typography>

            {/* 양식 다운로드 버튼 */}
            <Box sx={{ marginBottom: 3, textAlign: 'right' }}>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={handleDownloadTemplate}
                disabled={downloadingTemplate}
                sx={{ 
                  minWidth: 150,
                  backgroundColor: 'white',
                  '&:hover': {
                    backgroundColor: '#f5f5f5'
                  }
                }}
              >
                {downloadingTemplate ? (
                  <CircularProgress size={20} />
                ) : (
                  '업로드 양식 다운로드'
                )}
              </Button>
            </Box>

            {/* 파일 업로드 영역 */}
            <Paper
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                padding: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: '#fafafa',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                  borderColor: '#999',
                },
                marginBottom: 3,
              }}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={handleUploadAreaClick}
            >
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept=".xlsx,.xls"
                onChange={handleFileSelect}
              />
              
              
              <CloudUploadIcon sx={{ fontSize: 48, color: '#ccc', marginBottom: 2 }} />
              {selectedFile ? (
                <Box>
                  <Typography variant="h6" color="primary">
                    선택된 파일: {selectedFile.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    파일 크기: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </Typography>
                </Box>
              ) : (
                <Box>
                  <Typography variant="h6" color="textSecondary">
                    엑셀 파일을 업로드하세요
                  </Typography>
                </Box>
              )}
            </Paper>

            {/* HS코드 분류하기 버튼 */}
            {selectedFile && (
              <Box sx={{ textAlign: 'center' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleClassification}
                  disabled={uploading}
                  sx={{ 
                    minWidth: 200, 
                    minHeight: 50
                  }}
                >
                  {uploading ? (
                    <>
                      <CircularProgress size={20} sx={{ marginRight: 1 }} />
                      처리 중...
                    </>
                  ) : (
                    'HS코드 분류하기'
                  )}
                </Button>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* 분류 결과 */}
      {showResults && uploadResult && (
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ marginBottom: 2 }}>
              분류 결과
            </Typography>

            {/* 버튼들 */}
            <Box sx={{ display: 'flex', gap: 2, marginBottom: 3 }}>
              <Button
                variant="contained"
                startIcon={<DownloadIcon />}
                onClick={handleDownloadResult}
                sx={{ minWidth: 180 }}
              >
                분류 결과 엑셀 다운로드
              </Button>
              <Button
                variant="outlined"
                onClick={handleStartOver}
                sx={{ minWidth: 180 }}
              >
                다른 파일로 다시 시작하기
              </Button>
            </Box>
            
            <Box sx={{ marginBottom: 3 }}>
              <Typography variant="body1">
                <strong>파일명:</strong> {uploadResult.filename} | 
                <strong> 전체 건수:</strong> {uploadResult.total_count} | 
                <span style={{ color: '#2e7d32' }}><strong> 성공:</strong> {uploadResult.success_count}</span> | 
                <span style={{ color: '#d32f2f' }}><strong> 실패:</strong> {uploadResult.failed_count}</span>
              </Typography>
            </Box>
            
            {/* 결과 테이블 */}
            {tableData && tableData.length > 0 && (
              <TableContainer 
                component={Paper} 
                sx={{ 
                  marginTop: 3, 
                  maxHeight: 600, 
                  border: '1px solid #ddd'
                }}
              >
                <Table stickyHeader size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ backgroundColor: '#E8F3FF', fontWeight: 'bold', textAlign: 'center' }}>
                        수정여부
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('style_no')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          Style No
                          {renderSortIcon('style_no')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('product_name')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          이름
                          {renderSortIcon('product_name')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('weaving_type')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          소재타입
                          {renderSortIcon('weaving_type')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('category')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          카테고리
                          {renderSortIcon('category')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('gender')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          성별
                          {renderSortIcon('gender')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('composition')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          상세 성분
                          {renderSortIcon('composition')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('hs_code')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          HS Code
                          {renderSortIcon('hs_code')}
                        </Box>
                      </TableCell>
                      <TableCell 
                        sx={{ 
                          backgroundColor: '#E8F3FF', 
                          fontWeight: 'bold', 
                          textAlign: 'center',
                          cursor: 'pointer',
                          '&:hover': { backgroundColor: '#D1E7FF' }
                        }}
                        onClick={() => handleSort('note')}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          Note
                          {renderSortIcon('note')}
                        </Box>
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {tableData.map((row: TableRow, index: number) => (
                      <TableRow key={index} hover>
                        <TableCell>
                          {row.isModified && (
                            <CheckIcon sx={{ color: '#2e7d32', fontSize: 20 }} />
                          )}
                        </TableCell>
                        <TableCell>{row.style_no}</TableCell>
                        <TableCell>{row.product_name}</TableCell>
                        <TableCell>{row.weaving_type}</TableCell>
                        <TableCell>{row.category}</TableCell>
                        <TableCell>{row.gender}</TableCell>
                        <TableCell>{row.composition}</TableCell>
                        <TableCell 
                          sx={{
                            backgroundColor: row.hs_code === 'unknown' ? '#ffebee' : '#e8f5e8',
                            color: row.hs_code === 'unknown' ? '#c62828' : '#2e7d32',
                            cursor: 'pointer',
                            '&:hover': {
                              backgroundColor: row.hs_code === 'unknown' ? '#ffcdd2' : '#c8e6c8'
                            }
                          }}
                          onDoubleClick={() => handleHSCodeDoubleClick(index, row.hs_code)}
                          title="더블클릭하여 수정"
                        >
                          {row.hs_code}
                        </TableCell>
                        <TableCell>{row.note}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      )}

      {/* HS Code 편집 다이얼로그 */}
      <Dialog 
        open={editDialogOpen} 
        onClose={handleEditCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>HS Code 수정</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            원본 값: <strong>{originalValue}</strong>
          </Typography>
          <TextField
            autoFocus
            fullWidth
            label="HS Code"
            value={editedValue}
            onChange={(e) => setEditedValue(e.target.value)}
            variant="outlined"
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={handleEditCancel}
            startIcon={<CloseIcon />}
          >
            취소
          </Button>
          <Button 
            onClick={handleEditConfirm}
            variant="contained"
            startIcon={<CheckIcon />}
            disabled={editedValue === originalValue}
          >
            확인
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default HSClassification; 