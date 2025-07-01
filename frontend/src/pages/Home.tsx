import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid as MuiGrid,
  Button,
  useTheme,
  Container,
} from '@mui/material';
import {
  TableChart as TableChartIcon,
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Description as TemplateIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Grid = MuiGrid as any;  // 임시 해결책

const Home: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  const features = [
    {
      title: '의류 카테고리 관리',
      description: '의류 카테고리 정보를 관리하고 편집할 수 있습니다.',
      icon: <TableChartIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />,
      action: () => navigate('/categories'),
    },
    {
      title: '의류 성분 사전',
      description: '의류 성분 정보를 관리하고 검색할 수 있습니다.',
      icon: <CloudUploadIcon sx={{ fontSize: 40, color: theme.palette.secondary.main }} />,
      action: () => navigate('/fabric-components'),
    },
    {
      title: '계정 관리',
      description: '시스템 계정을 관리하고 권한을 설정할 수 있습니다.',
      icon: <DownloadIcon sx={{ fontSize: 40, color: theme.palette.success.main }} />,
      action: () => navigate('/accounts'),
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 6, textAlign: 'center' }}>
        <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
          의류 관리 시스템
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          의류 카테고리와 성분 정보를 체계적으로 관리하세요
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid component="div" item xs={12} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                p: 2,
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: theme.shadows[4],
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {feature.description}
                </Typography>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={feature.action}
                  sx={{ mt: 'auto' }}
                >
                  시작하기
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/categories')}
          startIcon={<TableChartIcon />}
        >
          카테고리 관리 시작하기
        </Button>
      </Box>
    </Container>
  );
};

export default Home; 