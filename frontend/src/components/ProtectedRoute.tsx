import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole?: string;
    allowedRoles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole, allowedRoles }) => {
    const { isAuthenticated, role } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/" state={{ from: location }} replace />;
    }

    // 특정 역할만 허용하는 경우
    if (requiredRole && role !== requiredRole) {
        // client는 HS 분류 페이지로 리다이렉트
        if (role === 'client') {
            return <Navigate to="/hs-classification" replace />;
        }
        return <Navigate to="/unauthorized" replace />;
    }

    // 허용된 역할 목록이 있는 경우
    if (allowedRoles && !allowedRoles.includes(role || '')) {
        // client는 HS 분류 페이지로 리다이렉트
        if (role === 'client') {
            return <Navigate to="/hs-classification" replace />;
        }
        return <Navigate to="/unauthorized" replace />;
    }

    return <>{children}</>;
};

export default ProtectedRoute; 