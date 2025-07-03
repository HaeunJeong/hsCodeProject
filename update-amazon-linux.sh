#!/bin/bash

echo "=== 시스템 업데이트 시작 (Amazon Linux 2) ==="

# 1. 백엔드 업데이트
echo "1. 백엔드 업데이트 중..."
cd /home/ec2-user/excel-project/backend

# 기존 프로세스 중지
pm2 stop excel-project-backend

# 가상환경 활성화
source venv/bin/activate

# 의존성 업데이트 (requirements.txt가 변경된 경우)
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python -m alembic upgrade head

# 프로세스 재시작
pm2 start ecosystem.config.js

echo "백엔드 업데이트 완료"

# 2. 프론트엔드 업데이트
echo "2. 프론트엔드 업데이트 중..."
cd /home/ec2-user/excel-project/frontend

# 의존성 업데이트 (package.json이 변경된 경우)
npm install

# 새로운 빌드
npm run build

# 기존 파일 제거 후 새 파일 복사
sudo rm -rf /var/www/html/*
sudo cp -r build/* /var/www/html/
sudo chown -R nginx:nginx /var/www/html/

echo "프론트엔드 업데이트 완료"

# 3. Nginx 재시작 (필요한 경우)
echo "3. Nginx 재시작..."
sudo systemctl reload nginx

echo "=== 업데이트 완료 ==="
echo "서비스 상태:"
pm2 status 