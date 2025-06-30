import React, { useState, useRef } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  Paper,
  CircularProgress,
  Alert,
  Stack
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { HotTable } from '@handsontable/react';
import { registerAllModules } from 'handsontable/registry';
import type { HotTableProps } from '@handsontable/react';
import 'handsontable/dist/handsontable.full.min.css';
import axios from 'axios';
import * as XLSX from 'xlsx';

// Handsontable 모듈 등록
registerAllModules();

const ExcelUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [data, setData] = useState<any[]>([]);
  const [headers, setHeaders] = useState<string[]>([]);
  const hotRef = useRef<any>(null);

  const readExcel = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        if (!data) {
          throw new Error('파일을 읽을 수 없습니다.');
        }

        const workbook = XLSX.read(data, { type: 'binary' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        
        // Convert Excel data to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        if (jsonData.length < 2) {
          throw new Error('데이터가 충분하지 않습니다.');
        }

        // First row as headers
        const headers = jsonData[0] as string[];
        
        // Rest of the rows as data
        const rows = jsonData.slice(1).map((row: any) => {
          return headers.reduce((obj: any, header: string, index: number) => {
            obj[header] = row[index] || '';
            return obj;
          }, {});
        });

        setHeaders(headers);
        setData(rows);
        setError(null);
      } catch (err) {
        setError('파일 읽기에 실패했습니다.');
        console.error('File reading error:', err);
        setData([]);
        setHeaders([]);
      }
    };
    reader.onerror = () => {
      setError('파일 읽기에 실패했습니다.');
      setData([]);
      setHeaders([]);
    };
    reader.readAsBinaryString(file);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedFile = event.target.files[0];
      if (selectedFile.name.endsWith('.xlsx') || 
          selectedFile.name.endsWith('.xls') || 
          selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        readExcel(selectedFile);
        setError(null);
      } else {
        setError('엑셀 또는 CSV 파일만 업로드 가능합니다.');
        setFile(null);
        setData([]);
        setHeaders([]);
      }
    }
  };

  const handleUpload = async () => {
    if (!file || !data.length) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/excel/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess(true);
    } catch (err) {
      setError('파일 업로드 중 오류가 발생했습니다.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const tableSettings: HotTableProps = {
    data: data,
    colHeaders: headers,
    rowHeaders: true,
    height: 'auto',
    width: '100%',
    licenseKey: 'non-commercial-and-evaluation',
    stretchH: 'all' as const,
    contextMenu: true,
    filters: true,
    dropdownMenu: true,
    readOnly: false,
    afterChange: (changes: any) => {
      if (changes) {
        // 데이터 변경 처리
        const newData = [...data];
        changes.forEach(([row, prop, oldValue, newValue]: [number, string, any, any]) => {
          newData[row][prop] = newValue;
        });
        setData(newData);
      }
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', mt: 4, p: 2 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Stack spacing={3}>
          <Typography variant="h5" gutterBottom align="center">
            엑셀 파일 업로드
          </Typography>
          
          <Box sx={{ textAlign: 'center' }}>
            <input
              accept=".xlsx,.xls,.csv"
              style={{ display: 'none' }}
              id="excel-file-input"
              type="file"
              onChange={handleFileChange}
            />
            <label htmlFor="excel-file-input">
              <Button
                variant="outlined"
                component="span"
                startIcon={<CloudUploadIcon />}
              >
                파일 선택
              </Button>
            </label>
            
            {file && (
              <Typography variant="body1" sx={{ mt: 1 }}>
                선택된 파일: {file.name}
              </Typography>
            )}
          </Box>

          {error && (
            <Alert severity="error">
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success">
              파일이 성공적으로 업로드되었습니다!
            </Alert>
          )}

          {data.length > 0 && (
            <Box sx={{ width: '100%', overflow: 'auto' }}>
              <HotTable {...tableSettings} ref={hotRef} />
            </Box>
          )}

          <Box sx={{ textAlign: 'center' }}>
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!file || loading || !data.length}
            >
              {loading ? <CircularProgress size={24} /> : '업로드'}
            </Button>
          </Box>
        </Stack>
      </Paper>
    </Box>
  );
};

export default ExcelUpload; 