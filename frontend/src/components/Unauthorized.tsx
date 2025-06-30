import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Unauthorized: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h4" gutterBottom>
          접근 권한이 없습니다
        </Typography>
        <Typography variant="body1" color="text.secondary" align="center" sx={{ mt: 2, mb: 4 }}>
          이 페이지에 접근할 수 있는 권한이 없습니다.
          관리자에게 문의하시기 바랍니다.
        </Typography>
        <Button
          variant="contained"
          onClick={() => navigate(-1)}
          sx={{ mt: 2 }}
        >
          이전 페이지로 돌아가기
        </Button>
      </Box>
    </Container>
  );
};

export default Unauthorized; 