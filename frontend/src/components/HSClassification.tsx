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
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';
import { hsClassificationApi } from '../services/api';

const HSClassification: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [downloadingTemplate, setDownloadingTemplate] = useState(false);
  const [alert, setAlert] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
        setAlert({ type: 'success', message: response.message || 'HS코드 분류가 완료되었습니다.' });
      } else {
        setAlert({ type: 'error', message: response.message || 'HS코드 분류 중 오류가 발생했습니다.' });
      }
    } catch (error) {
      setAlert({ type: 'error', message: 'HS코드 분류 중 오류가 발생했습니다.' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box sx={{ padding: 3 }}>

      {alert && (
        <Alert severity={alert.type} sx={{ marginBottom: 3 }}>
          {alert.message}
        </Alert>
      )}

          <Typography variant="h6" sx={{ marginBottom: 2, display: 'flex', alignItems: 'center' }}>
            <AssignmentIcon sx={{ marginRight: 1 }} />
            파일 업로드
          </Typography>

          {/* 양식 다운로드 버튼 */}
          <Box sx={{ marginBottom: 3, textAlign: 'right' }}>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleDownloadTemplate}
              disabled={downloadingTemplate}
              sx={{ minWidth: 150 }}
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
                  여기에 파일을 업로드하세요
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ marginTop: 1 }}>
                  Excel 파일을 드래그 앤 드롭하거나 클릭하여 선택하세요
                </Typography>
              </Box>
            )}
          </Paper>

          {/* HS코드 분류하기 버튼 */}
          <Box sx={{ textAlign: 'center' }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleClassification}
              disabled={!selectedFile || uploading}
              sx={{ minWidth: 200, minHeight: 50 }}
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

      {/* 분류 결과 */}
      {uploadResult && (
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ marginBottom: 2 }}>
              분류 결과
            </Typography>
            <Box sx={{ marginBottom: 2 }}>
              <Typography variant="body1">
                <strong>파일명:</strong> {uploadResult.filename}
              </Typography>
              <Typography variant="body1">
                <strong>전체 건수:</strong> {uploadResult.total_count}
              </Typography>
              <Typography variant="body1" color="success.main">
                <strong>성공:</strong> {uploadResult.success_count}
              </Typography>
              <Typography variant="body1" color="error.main">
                <strong>실패:</strong> {uploadResult.failed_count}
              </Typography>
            </Box>
            
            {/* 결과 테이블 */}
            {uploadResult.results && uploadResult.results.length > 0 && (
              <Box sx={{ marginTop: 3, overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                  <thead>
                    <tr style={{ backgroundColor: '#f5f5f5' }}>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>수정여부</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Style No</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>이름</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>소재타입</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>카테고리</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>성별</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>상세 성분</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>HS Code</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Note</th>
                    </tr>
                  </thead>
                  <tbody>
                    {uploadResult.results.map((result: any, index: number) => (
                      <tr key={index}>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}></td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.style_no}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.product_name}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.weaving_type}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.category}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.gender}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.composition}</td>
                        <td style={{ 
                          border: '1px solid #ddd', 
                          padding: '8px',
                          backgroundColor: result.hs_code === 'unknown' ? '#ffebee' : '#e8f5e8',
                          color: result.hs_code === 'unknown' ? '#c62828' : '#2e7d32'
                        }}>
                          {result.hs_code}
                        </td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{result.note}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Box>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default HSClassification; 