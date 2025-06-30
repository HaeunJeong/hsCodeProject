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
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  useTheme,
  Divider,
  Button,
  Chip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  TableChart as TableChartIcon,
  Person as PersonIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  ManageAccounts as ManageAccountsIcon,
  Login as LoginIcon,
  Logout as LogoutIcon,
  Description as TemplateIcon,
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
    { text: '홈', path: '/', icon: <HomeIcon /> },
    { text: 'HS코드 매핑', path: '/mapping', icon: <TableChartIcon /> },
    { text: '의류 카테고리 사전', path: '/categories', icon: <TableChartIcon /> },
    ...(role === 'admin' ? [
      { text: '계정 관리', path: '/accounts', icon: <ManageAccountsIcon /> }
    ] : [])
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
    navigate('/login');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          backgroundColor: 'white',
          color: 'text.primary',
          boxShadow: 1,
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
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            HS코드 자동분류 시스템
          </Typography>
          
          {isAuthenticated ? (
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
              <Button
                variant="outlined"
                color="inherit"
                startIcon={<LogoutIcon />}
                onClick={handleLogout}
              >
                로그아웃
              </Button>
            </Box>
          ) : (
            <Button
              variant="contained"
              color="primary"
              startIcon={<LoginIcon />}
              onClick={handleLogin}
            >
              로그인
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: theme.palette.grey[50],
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                onClick={() => navigate(item.path)}
                selected={location.pathname === item.path}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: theme.palette.primary.light,
                    color: theme.palette.primary.main,
                    '&:hover': {
                      backgroundColor: theme.palette.primary.light,
                    },
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: location.pathname === item.path ? theme.palette.primary.main : 'inherit',
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
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