import React from 'react';
import { Box, Typography, Grid as MuiGrid, Paper } from '@mui/material';
import {
  LibraryBooks as MappingIcon,
  Book as DictionaryIcon,
  Description as TemplateIcon,
  VpnKey as AccessCodeIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Grid = MuiGrid as any;  // 임시 해결책

interface DashboardCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, description, icon, path }) => {
  const navigate = useNavigate();

  return (
    <Paper
      sx={{
        p: 3,
        display: 'flex',
        flexDirection: 'column',
        height: 200,
        cursor: 'pointer',
        '&:hover': {
          backgroundColor: 'action.hover',
        },
      }}
      onClick={() => navigate(path)}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Box sx={{ mr: 2, color: 'primary.main' }}>{icon}</Box>
        <Typography variant="h6" component="h2">
          {title}
        </Typography>
      </Box>
      <Typography variant="body2" color="text.secondary">
        {description}
      </Typography>
    </Paper>
  );
};

const Dashboard: React.FC = () => {
  const { role } = useAuth();

  const dashboardItems = [
    {
      title: 'HS코드 매핑관리',
      description: 'HS코드 자동 분류를 위한 매핑 규칙을 관리합니다. 엑셀 파일을 업로드하고 결과를 확인할 수 있습니다.',
      icon: <MappingIcon fontSize="large" />,
      path: '/mapping-rules',
    },
    {
      title: '의류 분류 사전',
      description: '의류 분류를 위한 용어 사전을 관리합니다. 새로운 용어를 추가하고 기존 용어를 수정할 수 있습니다.',
      icon: <DictionaryIcon fontSize="large" />,
      path: '/dictionary',
    },
    ...(role === 'admin' ? [
      {
        title: '계정 코드 관리',
        description: '시스템 접근을 위한 계정 코드를 관리합니다. 새로운 코드를 생성하고 기존 코드를 관리할 수 있습니다.',
        icon: <AccessCodeIcon fontSize="large" />,
        path: '/access-codes',
      },
    ] : []),
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        대시보드
      </Typography>
      <Grid container spacing={3}>
        {dashboardItems.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.path}>
            <DashboardCard {...item} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Dashboard; 