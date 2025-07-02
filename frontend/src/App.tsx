import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import Layout from './components/Layout';
import Home from './pages/Home';

import AccountManager from './components/AccountManager';
import StandardCategoryManager from './components/StandardCategoryManager';
import FabricComponentManager from './components/FabricComponentManager';
import HSClassification from './components/HSClassification';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';

const theme = createTheme({
  palette: {
    primary: {
      main: '#5BA7F7',
      light: '#B8D5FA',
      dark: '#2E7BF0',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#9DCBF9',
      light: '#C7E0FB',
      dark: '#6B9AF5',
    },
    background: {
      default: '#F5F7FA',
      paper: '#FFFFFF',
    },
    grey: {
      50: '#F4F9FF',
      100: '#E8F3FF',
      200: '#D1E7FF',
      300: '#A3D0FF',
      400: '#75B8FF',
      500: '#5BA7F7',
      600: '#4285F4',
      700: '#1976D2',
      800: '#1565C0',
      900: '#0D47A1',
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
        contained: {
          background: 'linear-gradient(135deg, #5BA7F7 0%, #4285F4 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #4285F4 0%, #2E7BF0 100%)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          border: '1px solid #E8F3FF',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%)',
          borderBottom: '1px solid #E8F3FF',
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
            <Route element={<Layout />}>
              <Route 
                path="/" 
                element={<Home />} 
              />
              <Route 
                path="/hs-classification" 
                element={
                  <ProtectedRoute allowedRoles={["admin", "client"]}>
                    <HSClassification />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/categories" 
                element={
                  <ProtectedRoute allowedRoles={["admin"]}>
                    <StandardCategoryManager />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/fabric-components" 
                element={
                  <ProtectedRoute allowedRoles={["admin"]}>
                    <FabricComponentManager />
                  </ProtectedRoute>
                } 
              />
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
