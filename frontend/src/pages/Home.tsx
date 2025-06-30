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
      title: 'HS코드 자동 분류',
      description: '의류 상품 정보를 기반으로 HS코드를 자동으로 분류합니다.',
      icon: <TableChartIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />,
      action: () => navigate('/mapping'),
    },
    {
      title: '엑셀 파일 업로드',
      description: '대량의 상품 데이터를 엑셀 파일로 한 번에 처리할 수 있습니다.',
      icon: <CloudUploadIcon sx={{ fontSize: 40, color: theme.palette.secondary.main }} />,
      action: () => navigate('/mapping'),
    },
    {
      title: '결과 다운로드',
      description: '분류된 HS코드를 포함한 결과를 엑셀 파일로 다운로드할 수 있습니다.',
      icon: <DownloadIcon sx={{ fontSize: 40, color: theme.palette.success.main }} />,
      action: () => navigate('/mapping'),
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 6, textAlign: 'center' }}>
        <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
          HS코드 자동분류 시스템
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          의류 상품 정보를 기반으로 HS코드를 자동으로 분류하고 관리하세요
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
          onClick={() => navigate('/mapping')}
          startIcon={<TableChartIcon />}
        >
          HS코드 분류 시작하기
        </Button>
      </Box>
    </Container>
  );
};

export default Home; 