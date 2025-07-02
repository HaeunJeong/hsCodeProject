import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  Typography,
  useTheme,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })<{
  open?: boolean;
}>(({ theme, open }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  backgroundColor: '#F5F7FA',
  minHeight: '100vh',
  transition: theme.transitions.create('margin', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  marginLeft: `-${drawerWidth}px`,
  ...(open && {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

interface LayoutProps {}

const Layout: React.FC<LayoutProps> = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, role, logout } = useAuth();
  const [open, setOpen] = useState(true);

  console.log('Layout - 현재 인증 상태:', { isAuthenticated, role });

  const menuItems = [
    // 비로그인 상태에서는 홈만 접근 가능
    ...(!isAuthenticated ? [
      { text: '홈', path: '/' }
    ] : [
      // client 권한은 홈과 HS코드 자동분류만 접근 가능
      ...(role === 'client' ? [
        { text: '홈', path: '/' },
        { text: 'HS코드 자동분류', path: '/hs-classification' }
      ] : [
        // admin 권한은 모든 메뉴 접근 가능
        { text: '홈', path: '/' },
        { text: 'HS코드 자동분류', path: '/hs-classification' },
        { text: '의류 카테고리 관리', path: '/categories' },
        { text: '의류 성분 사전', path: '/fabric-components' },
        { text: '계정 관리', path: '/accounts' }
      ])
    ])
  ];

  console.log('Layout - 메뉴 아이템:', menuItems);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleLogin = () => {
    navigate('/');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          backgroundColor: 'transparent',
          color: 'text.primary',
          boxShadow: 'none',
          zIndex: (theme) => theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
            <img 
              src="/haebom-logo.png" 
              alt="HAEBOM HS코드 자동분류 시스템" 
              style={{ 
                height: '60px', 
                width: 'auto', 
                cursor: 'pointer' 
              }}
              onClick={() => navigate('/')}
            />
          </Box>
        
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography
                  component="span"
                  sx={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    height: '24px',
                    padding: '0 12px',
                    fontSize: '0.8125rem',
                    borderRadius: '16px',
                    backgroundColor: role === 'admin' ? '#e3f2fd' : '#f5f5f5',
                    color: role === 'admin' ? '#1976d2' : '#757575',
                    border: '1px solid',
                    borderColor: role === 'admin' ? '#bbdefb' : '#e0e0e0',
                  }}
                >
                  {role === 'admin' ? '관리자' : '일반 사용자'}
                </Typography>
              </Box>
            </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: '#FFFFFF',
            borderRight: '1px solid #E0E0E0',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose} sx={{ color: '#5BA7F7' }}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider sx={{ borderColor: '#E0E0E0' }} />
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                onClick={() => navigate(item.path)}
                selected={location.pathname === item.path}
                sx={{
                  pl: 4,
                  pr: 1,
                  py: 1.5,
                  '&.Mui-selected': {
                    backgroundColor: '#5BA7F7',
                    color: '#FFFFFF',
                    '&:hover': {
                      backgroundColor: '#4285F4',
                    },
                  },
                  '&:hover': {
                    backgroundColor: '#F5F5F5',
                  },
                }}
              >
                <ListItemText 
                  primary={item.text}
                  sx={{
                    '& .MuiListItemText-primary': {
                      fontWeight: location.pathname === item.path ? 700 : 600,
                      color: location.pathname === item.path ? '#FFFFFF' : 'inherit',
                    }
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Main open={open}>
        <DrawerHeader />
        <Outlet />
      </Main>
    </Box>
  );
};

export default Layout; 