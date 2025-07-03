#!/bin/bash

echo "=== 환경 변수 설정 ==="

# 백엔드 .env 파일 생성
echo "백엔드 환경 변수 파일을 생성합니다..."

cat > /home/ubuntu/excel-project/backend/.env << 'EOL'
# 데이터베이스 설정 (AWS RDS)
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname

# JWT 설정
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 환경 설정
ENVIRONMENT=production
EOL

echo "✅ backend/.env 파일이 생성되었습니다."
echo ""
echo "🔧 다음 값들을 실제 값으로 수정해주세요:"
echo "📝 nano /home/ubuntu/excel-project/backend/.env"
echo ""
echo "필수 수정 항목:"
echo "1. DATABASE_URL - AWS RDS PostgreSQL 연결 정보"
echo "2. SECRET_KEY - JWT 토큰 암호화 키"
echo ""
echo "예시:"
echo "DATABASE_URL=postgresql://myuser:mypass@my-rds-endpoint.amazonaws.com:5432/haebom_db"
echo "SECRET_KEY=$(openssl rand -base64 32)"
echo ""
echo "수정 완료 후 다음 명령어로 배포하세요:"
echo "chmod +x /home/ubuntu/excel-project/deploy-from-git.sh"
echo "/home/ubuntu/excel-project/deploy-from-git.sh" 