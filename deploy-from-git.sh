#!/bin/bash

# Git 기반 자동 배포 스크립트
echo "=== Git 기반 자동 배포 시작 ==="

# 설정 변수
PROJECT_DIR="/home/ubuntu/excel-project"
GIT_REPO="https://github.com/HaeunJeong/hsCodeProject.git"  # 실제 Git 저장소 URL로 변경
BRANCH="main"  # 또는 master

# 1. 프로젝트 디렉토리 확인 및 이동
if [ -d "$PROJECT_DIR" ]; then
    echo "1. 기존 프로젝트 업데이트 중..."
    cd $PROJECT_DIR
    
    # Git 상태 확인
    if [ -d ".git" ]; then
        # 기존 변경사항 백업 (혹시 있을 경우)
        git stash
        
        # 최신 코드 가져오기
        git pull origin $BRANCH
        
        # 백업한 변경사항 복원 (필요시)
        # git stash pop
    else
        echo "Git 저장소가 아닙니다. 다시 클론합니다."
        cd /home/ubuntu
        rm -rf excel-project
        git clone $GIT_REPO excel-project
        cd excel-project
    fi
else
    echo "1. 프로젝트 최초 클론 중..."
    cd /home/ubuntu
    git clone $GIT_REPO excel-project
    cd excel-project
fi

# 2. 환경 변수 파일 확인
echo "2. 환경 변수 파일 확인 중..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️  backend/.env 파일이 없습니다. 환경 변수를 설정해주세요."
    cat > backend/.env << EOL
# 데이터베이스 설정 (AWS RDS)
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname

# JWT 설정
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 환경 설정
ENVIRONMENT=production
EOL
    echo "backend/.env 파일이 생성되었습니다. 실제 값으로 수정해주세요."
    echo "배포를 계속하려면 backend/.env 파일을 수정한 후 다시 실행하세요."
    exit 1
fi

# 3. 백엔드 배포
echo "3. 백엔드 배포 중..."
cd backend

# 기존 프로세스 중지
pm2 stop excel-project-backend || true

# 가상환경 활성화
source venv/bin/activate || {
    echo "가상환경이 없습니다. 새로 생성합니다."
    python3 -m venv venv
    source venv/bin/activate
}

# 의존성 설치
pip install --upgrade pip
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python -m alembic upgrade head

# PM2 설정 파일 업데이트
cat > ecosystem.config.js << EOL
module.exports = {
  apps: [{
    name: 'excel-project-backend',
    script: 'uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: '/home/ubuntu/excel-project/backend',
    interpreter: '/home/ubuntu/excel-project/backend/venv/bin/python',
    env: {
      PYTHONPATH: '/home/ubuntu/excel-project/backend'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: '/home/ubuntu/logs/backend-error.log',
    out_file: '/home/ubuntu/logs/backend-out.log',
    log_file: '/home/ubuntu/logs/backend.log'
  }]
};
EOL

# 로그 디렉토리 생성
mkdir -p /home/ubuntu/logs

# 백엔드 시작
pm2 start ecosystem.config.js

# 4. 프론트엔드 배포
echo "4. 프론트엔드 배포 중..."
cd ../frontend

# 환경 변수 파일 생성
cat > .env << EOL
# API 서버 주소 (Nginx 프록시 사용으로 상대 경로 사용)
REACT_APP_API_URL=

# 기타 환경 변수
REACT_APP_ENVIRONMENT=production
EOL

# 의존성 설치
npm install

# 프로덕션 빌드
npm run build

# Nginx 웹 디렉토리로 빌드 파일 복사
sudo rm -rf /var/www/html/*
sudo cp -r build/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html/

# 5. Nginx 설정 업데이트
echo "5. Nginx 설정 업데이트 중..."
cd ..
sudo cp nginx.conf /etc/nginx/sites-available/excel-project
sudo ln -sf /etc/nginx/sites-available/excel-project /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx 설정 테스트 및 재시작
sudo nginx -t && sudo systemctl reload nginx

# 6. 배포 완료
echo "=== 배포 완료 ==="
echo "백엔드 상태: $(pm2 status | grep excel-project-backend)"
echo "웹사이트: http://13.209.30.21"
echo "API 문서: http://13.209.30.21/docs"
echo ""
echo "로그 확인:"
echo "- 백엔드 로그: pm2 logs excel-project-backend"
echo "- Nginx 로그: sudo tail -f /var/log/nginx/error.log" 