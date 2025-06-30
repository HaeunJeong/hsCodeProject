import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import Layout from './components/Layout';
import Home from './pages/Home';
import MappingRuleManager from './components/MappingRuleManager';
import AccountManager from './components/AccountManager';
import StandardCategoryManager from './components/StandardCategoryManager';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/Login';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
      light: '#e3f2fd',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      'Pretendard Variable',
      'Pretendard',
      '-apple-system',
      'BlinkMacSystemFont',
      'system-ui',
      'Roboto',
      '"Helvetica Neue"',
      '"Segoe UI"',
      '"Apple SD Gothic Neo"',
      '"Noto Sans KR"',
      '"Malgun Gothic"',
      'sans-serif',
    ].join(','),
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.03em',
    },
    h5: {
      fontWeight: 600,
      letterSpacing: '-0.03em',
    },
    h6: {
      fontWeight: 600,
      letterSpacing: '-0.03em',
    },
    subtitle1: {
      letterSpacing: '-0.03em',
    },
    body1: {
      letterSpacing: '-0.03em',
    },
    body2: {
      letterSpacing: '-0.03em',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/mapping" element={<MappingRuleManager />} />
              <Route path="/categories" element={<StandardCategoryManager />} />
              <Route 
                path="/accounts" 
                element={
                  <ProtectedRoute requiredRole="admin">
                    <AccountManager />
                  </ProtectedRoute>
                } 
              />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
