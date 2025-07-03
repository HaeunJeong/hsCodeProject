#!/bin/bash

echo "=== 프론트엔드 배포 시작 ==="

# 프론트엔드 디렉토리로 이동
cd /home/ubuntu/excel-project/frontend

# 환경변수 파일 생성
cat > .env << EOL
# API 서버 주소 (Nginx 프록시 사용으로 상대 경로 사용)
REACT_APP_API_URL=

# 기타 환경 변수
REACT_APP_ENVIRONMENT=production
EOL

echo "환경변수 파일(.env)을 생성했습니다. EC2 IP로 수정해주세요."

# 의존성 설치
npm install

# 프로덕션 빌드
npm run build

# Nginx 웹 디렉토리로 빌드 파일 복사
sudo rm -rf /var/www/html/*
sudo cp -r build/* /var/www/html/

# Nginx 소유권 설정
sudo chown -R www-data:www-data /var/www/html/

echo "=== 프론트엔드 빌드 완료 ==="
echo "빌드된 파일이 /var/www/html에 배포되었습니다." 