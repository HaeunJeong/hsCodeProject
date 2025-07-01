import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid as MuiGrid,
  Button,
  useTheme,
  Container,
  TextField,
  Paper,
  Alert,
} from '@mui/material';
import {
  TableChart as TableChartIcon,
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Description as TemplateIcon,
  Login as LoginIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Grid = MuiGrid as any;  // 임시 해결책

const Home: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { isAuthenticated, role, login, logout, error: authError } = useAuth();
  const [accessCode, setAccessCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [inputError, setInputError] = useState('');

  const handleLogin = async () => {
    if (!accessCode.trim()) {
      setInputError('접속코드를 입력해주세요');
      return;
    }

    setInputError('');
    setLoading(true);

    try {
      const success = await login(accessCode.trim());
      if (success) {
        setAccessCode('');
      }
    } catch (err: any) {
      console.error('로그인 오류:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  // 비로그인 상태 UI
  if (!isAuthenticated) {
    return (
      <Container maxWidth="sm" sx={{ mt: 8, mb: 4 }}>
        <Paper 
          elevation={0} 
          sx={{ 
            p: 6, 
            textAlign: 'center',
            backgroundColor: 'transparent'
          }}
        >
          <Typography variant="h5" sx={{ mb: 4, fontWeight: 600 }}>
            로그인 코드를 입력해주세요
          </Typography>
          
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="접속 코드 입력"
              value={accessCode}
              onChange={(e) => {
                setAccessCode(e.target.value);
                if (inputError) setInputError('');
              }}
              onKeyPress={handleKeyPress}
              disabled={loading}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                }
              }}
            />
          </Box>

          {(authError || inputError) && (
            <Alert severity="error" sx={{ mb: 3, textAlign: 'left' }}>
              {authError || inputError}
            </Alert>
          )}

          <Button
            variant="contained"
            size="large"
            onClick={handleLogin}
            disabled={loading}
            sx={{
              py: 1.5,
              borderRadius: 2,
              fontWeight: 600,
            }}
          >
            {loading ? '접속 중...' : '접속하기'}
          </Button>
        </Paper>
      </Container>
    );
  }

  // 로그인된 상태 UI
  return (
    <Container maxWidth="sm" sx={{ mt: 8, mb: 4 }}>
      <Paper 
        elevation={0} 
        sx={{ 
          p: 6, 
          textAlign: 'center',
          backgroundColor: 'transparent'
        }}
      >
        <Typography variant="h5" sx={{ mb: 4, fontWeight: 600 }}>
          로그인 상태입니다
        </Typography>
        
        <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Typography
            component="span"
            sx={{
              display: 'inline-flex',
              alignItems: 'center',
              height: '32px',
              padding: '0 16px',
              fontSize: '0.875rem',
              borderRadius: '20px',
              backgroundColor: role === 'admin' ? '#e3f2fd' : '#f5f5f5',
              color: role === 'admin' ? '#1976d2' : '#757575',
              border: '1px solid',
              borderColor: role === 'admin' ? '#bbdefb' : '#e0e0e0',
              fontWeight: 600,
            }}
          >
            {role === 'admin' ? '관리자' : '일반 사용자'}
          </Typography>
        </Box>

        <Button
          variant="contained"
          size="large"
          onClick={handleLogout}
          startIcon={<LogoutIcon />}
          sx={{
            py: 1.5,
            borderRadius: 2,
            fontWeight: 600,
          }}
        >
          로그아웃 하기
        </Button>
      </Paper>
    </Container>
  );
};

export default Home; 