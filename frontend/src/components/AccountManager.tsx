import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Typography,
  Alert,
  CircularProgress,
  Chip,
  Snackbar,
  Radio,
  RadioGroup,
  FormControl,
  FormLabel,
  Select,
  MenuItem,
  InputLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ContentCopy as ContentCopyIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { IAccount, IAccountCreateData, IAccountUpdateData } from '../types/account';
import { accountApi } from '../services/api';

const initialFormData: IAccountCreateData = {
  name: '',
  code: '',
  role: 'client',
  isActive: true,
};

const AccountManager: React.FC = () => {
  const [accounts, setAccounts] = useState<IAccount[]>([]);
  const [filteredAccounts, setFilteredAccounts] = useState<IAccount[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState<IAccountCreateData>(initialFormData);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [copySuccess, setCopySuccess] = useState<string | null>(null);
  
  // 검색 관련 상태
  const [searchFilters, setSearchFilters] = useState({
    userType: 'all',  // 'all', 'active', 'inactive'
    role: 'all',      // 'all', 'admin', 'client'
    code: '',
    name: ''
  });

  const loadAccounts = async () => {
    try {
      setLoading(true);
      const data = await accountApi.getAccounts();
      setAccounts(data);
      setFilteredAccounts(data); // 초기에는 모든 데이터 표시
    } catch (error) {
      setError('계정 목록을 불러오는데 실패했습니다.');
      console.error('계정 목록 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleSearchChange = (field: string, value: string) => {
    setSearchFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 검색 버튼 클릭 시에만 실행되는 검색 함수
  const handleSearch = () => {
    let filtered = accounts;

    // 사용여부 필터 (AND 조건)
    if (searchFilters.userType !== 'all') {
      const isActive = searchFilters.userType === 'active';
      filtered = filtered.filter(account => account.isActive === isActive);
    }

    // 권한 필터 (AND 조건)
    if (searchFilters.role !== 'all') {
      filtered = filtered.filter(account => account.role === searchFilters.role);
    }

    // 계정 코드 검색 (AND 조건)
    if (searchFilters.code.trim()) {
      filtered = filtered.filter(account => 
        account.code.toLowerCase().includes(searchFilters.code.toLowerCase())
      );
    }

    // 이름 검색 (AND 조건)
    if (searchFilters.name.trim()) {
      filtered = filtered.filter(account => 
        account.name.toLowerCase().includes(searchFilters.name.toLowerCase())
      );
    }

    setFilteredAccounts(filtered);
  };

  // 새로운 데이터를 기반으로 검색을 적용하는 함수
  const applySearchToNewData = (newData: IAccount[]) => {
    let filtered = newData;

    // 사용여부 필터 (AND 조건)
    if (searchFilters.userType !== 'all') {
      const isActive = searchFilters.userType === 'active';
      filtered = filtered.filter(account => account.isActive === isActive);
    }

    // 권한 필터 (AND 조건)
    if (searchFilters.role !== 'all') {
      filtered = filtered.filter(account => account.role === searchFilters.role);
    }

    // 계정 코드 검색 (AND 조건)
    if (searchFilters.code.trim()) {
      filtered = filtered.filter(account => 
        account.code.toLowerCase().includes(searchFilters.code.toLowerCase())
      );
    }

    // 이름 검색 (AND 조건)
    if (searchFilters.name.trim()) {
      filtered = filtered.filter(account => 
        account.name.toLowerCase().includes(searchFilters.name.toLowerCase())
      );
    }

    return filtered;
  };

  const handleOpenDialog = (account?: IAccount) => {
    if (account) {
      setFormData({
        name: account.name,
        code: account.code,
        role: account.role,
        isActive: account.isActive,
      });
      setEditingId(account.id);
    } else {
      setFormData(initialFormData);
      setEditingId(null);
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
      
      if (editingId) {
        await accountApi.updateAccount(editingId, formData);
        setSuccess('계정이 수정되었습니다.');
      } else {
        await accountApi.createAccount(formData);
        setSuccess('새 계정이 생성되었습니다.');
      }
      
      handleCloseDialog();
      
      // 데이터 새로고침 후 검색 조건 적용
      const data = await accountApi.getAccounts();
      setAccounts(data);
      const filteredData = applySearchToNewData(data);
      setFilteredAccounts(filteredData);
      
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || '계정 저장에 실패했습니다.';
      setError(errorMessage);
      console.error('계정 저장 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('정말 이 계정을 삭제하시겠습니까?')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await accountApi.deleteAccount(id);
      setSuccess('계정이 삭제되었습니다.');
      
      // 수정 다이얼로그가 열려있다면 닫기
      if (openDialog) {
        handleCloseDialog();
      }
      
      // 데이터 새로고침 후 검색 조건 적용
      const data = await accountApi.getAccounts();
      setAccounts(data);
      const filteredData = applySearchToNewData(data);
      setFilteredAccounts(filteredData);
      
    } catch (error) {
      setError('계정 삭제에 실패했습니다.');
      console.error('계정 삭제 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  // 사용여부 토글 처리
  const handleToggleActive = async (id: number, currentStatus: boolean) => {
    try {
      setLoading(true);
      setError(null);
      
      const account = accounts.find(acc => acc.id === id);
      if (!account) return;

      await accountApi.updateAccount(id, {
        name: account.name,
        code: account.code,
        role: account.role,
        isActive: !currentStatus
      });
      
      setSuccess(`계정이 ${!currentStatus ? '활성화' : '비활성화'}되었습니다.`);
      
      // 데이터 새로고침 후 검색 조건 적용
      const data = await accountApi.getAccounts();
      setAccounts(data);
      const filteredData = applySearchToNewData(data);
      setFilteredAccounts(filteredData);
      
    } catch (error) {
      setError('계정 상태 변경에 실패했습니다.');
      console.error('계정 상태 변경 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyCode = async (code: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopySuccess('코드가 클립보드에 복사되었습니다.');
    } catch (err) {
      setError('코드 복사에 실패했습니다.');
    }
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 3 }}>
        계정 코드 관리
      </Typography>

      {/* 검색 영역 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, alignItems: 'flex-end' }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>사용여부</InputLabel>
              <Select
                value={searchFilters.userType}
                label="사용여부"
                onChange={(e) => handleSearchChange('userType', e.target.value)}
              >
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="active">사용</MenuItem>
                <MenuItem value="inactive">미사용</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>권한</InputLabel>
              <Select
                value={searchFilters.role}
                label="권한"
                onChange={(e) => handleSearchChange('role', e.target.value)}
              >
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="admin">관리자</MenuItem>
                <MenuItem value="client">고객사</MenuItem>
              </Select>
            </FormControl>

            <TextField
              size="small"
              label="계정 코드"
              value={searchFilters.code}
              onChange={(e) => handleSearchChange('code', e.target.value)}
              sx={{ minWidth: 150 }}
            />

            <TextField
              size="small"
              label="이름"
              value={searchFilters.name}
              onChange={(e) => handleSearchChange('name', e.target.value)}
              sx={{ minWidth: 150 }}
            />
          </Box>

          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<SearchIcon />}
              onClick={handleSearch}
              size="small"
            >
              검색
            </Button>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog()}
              size="small"
            >
              추가하기
            </Button>
          </Box>
        </Box>
      </Paper>

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

      {/* 결과 테이블 */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell sx={{ fontWeight: 'bold' }}>사용여부</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>계정 코드</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>이름</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>권한</TableCell>
              <TableCell sx={{ fontWeight: 'bold', textAlign: 'center' }}>관리</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAccounts.map((account) => (
              <TableRow key={account.id} hover>
                <TableCell>
                  <Switch
                    checked={account.isActive}
                    size="small"
                    onChange={() => handleToggleActive(account.id, account.isActive)}
                    disabled={loading}
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={account.code}
                    color="primary"
                    variant="outlined"
                    size="small"
                    onClick={() => handleCopyCode(account.code)}
                    clickable
                    sx={{ cursor: 'pointer' }}
                  />
                </TableCell>
                <TableCell>{account.name}</TableCell>
                <TableCell>
                  <Typography
                    component="span"
                    sx={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      height: '24px',
                      padding: '0 12px',
                      fontSize: '0.8125rem',
                      borderRadius: '16px',
                      backgroundColor: account.role === 'admin' ? '#e3f2fd' : '#f5f5f5',
                      color: account.role === 'admin' ? '#1976d2' : '#757575',
                      border: '1px solid',
                      borderColor: account.role === 'admin' ? '#bbdefb' : '#e0e0e0',
                    }}
                  >
                    {account.role === 'admin' ? '관리자' : '고객사'}
                  </Typography>
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    onClick={() => handleOpenDialog(account)}
                    sx={{ mr: 1 }}
                  >
                    <EditIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
            {filteredAccounts.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 3 }}>
                  검색 결과가 없습니다.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* 등록/수정 다이얼로그 */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingId ? '계정 수정' : '계정 코드 수정'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="계정 코드"
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              required
              helperText="영문 대문자와 숫자로 구성된 고유한 코드를 입력하세요"
              disabled={editingId !== null} // 수정 시에는 코드 변경 불가
            />
            <TextField
              fullWidth
              label="이름"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <FormControl component="fieldset">
              <FormLabel component="legend">권한</FormLabel>
              <RadioGroup
                row
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              >
                <FormControlLabel 
                  value="client" 
                  control={<Radio />} 
                  label="고객사" 
                />
                <FormControlLabel 
                  value="admin" 
                  control={<Radio />} 
                  label="관리자" 
                />
              </RadioGroup>
            </FormControl>
            <FormControlLabel
              control={
                <Switch
                  checked={formData.isActive}
                  onChange={(e) => setFormData({ ...formData, isActive: e.target.checked })}
                />
              }
              label="사용 여부"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
            <Box>
              {editingId && (
                <Button 
                  onClick={() => handleDelete(editingId)}
                  color="error"
                  startIcon={<DeleteIcon />}
                  disabled={loading}
                >
                  삭제
                </Button>
              )}
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button onClick={handleCloseDialog}>취소</Button>
              <Button 
                onClick={handleSubmit} 
                variant="contained"
                disabled={!formData.name || !formData.code || loading}
              >
                저장
              </Button>
            </Box>
          </Box>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={!!copySuccess}
        autoHideDuration={2000}
        onClose={() => setCopySuccess(null)}
        message={copySuccess}
      />
    </Box>
  );
};

export default AccountManager; 