import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container, Paper, Alert } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
    const [accessCode, setAccessCode] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { login, error } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!accessCode.trim()) {
            return;
        }

        setIsSubmitting(true);
        const success = await login(accessCode.trim());
        setIsSubmitting(false);

        if (success) {
            // 로그인 성공 시 페이지 이동
            const from = location.state?.from?.pathname || '/';
            navigate(from, { replace: true });
        }
    };

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
                <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
                    <Typography component="h1" variant="h5" sx={{ mb: 3 }}>
                        HS코드 자동 분류 시스템
                    </Typography>
                    {error && (
                        <Alert 
                            severity="error" 
                            sx={{ 
                                mb: 2,
                                '& .MuiAlert-message': {
                                    width: '100%'
                                }
                            }}
                        >
                            {error}
                        </Alert>
                    )}
                    <Box component="form" onSubmit={handleSubmit} noValidate>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="accessCode"
                            label="접속 코드"
                            name="accessCode"
                            autoFocus
                            value={accessCode}
                            onChange={(e) => setAccessCode(e.target.value)}
                            disabled={isSubmitting}
                            error={!!error}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? '로그인 중...' : '로그인'}
                        </Button>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
};

export default Login; 