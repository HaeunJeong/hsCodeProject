#!/bin/bash

echo "=== 백엔드 배포 시작 (Amazon Linux 2) ==="

# 백엔드 디렉토리로 이동
cd /home/ec2-user/excel-project/backend

# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt

# 환경변수 파일 생성 (필요시 수정)
cat > .env << EOL
# 데이터베이스 설정 (AWS RDS)
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname

# JWT 설정
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 환경 설정
ENVIRONMENT=production
EOL

echo "환경변수 파일(.env)을 생성했습니다. 실제 값으로 수정해주세요."

# 데이터베이스 마이그레이션
echo "데이터베이스 마이그레이션을 실행합니다..."
python -m alembic upgrade head

# PM2 설정 파일 생성
cat > ecosystem.config.js << EOL
module.exports = {
  apps: [{
    name: 'excel-project-backend',
    script: 'uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: '/home/ec2-user/excel-project/backend',
    interpreter: '/home/ec2-user/excel-project/backend/venv/bin/python',
    env: {
      PYTHONPATH: '/home/ec2-user/excel-project/backend'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: '/home/ec2-user/logs/backend-error.log',
    out_file: '/home/ec2-user/logs/backend-out.log',
    log_file: '/home/ec2-user/logs/backend.log'
  }]
};
EOL

# 로그 디렉토리 생성
mkdir -p /home/ec2-user/logs

echo "=== 백엔드 설정 완료 ==="
echo "PM2로 백엔드를 시작하려면: pm2 start ecosystem.config.js" 