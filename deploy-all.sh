#!/bin/bash

echo "=== HAEBOM HS코드 자동분류 시스템 배포 시작 ==="

# 1. Nginx 설정 파일 복사
echo "1. Nginx 설정 중..."
sudo cp nginx.conf /etc/nginx/sites-available/excel-project
sudo ln -sf /etc/nginx/sites-available/excel-project /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx 설정 테스트
sudo nginx -t
if [ $? -ne 0 ]; then
    echo "Nginx 설정 오류가 있습니다. 설정을 확인해주세요."
    exit 1
fi

# 2. 백엔드 배포
echo "2. 백엔드 배포 중..."
cd /home/ubuntu/excel-project/backend
chmod +x deploy.sh
./deploy.sh

# 3. 프론트엔드 배포
echo "3. 프론트엔드 배포 중..."
cd /home/ubuntu/excel-project/frontend
chmod +x deploy.sh
./deploy.sh

# 4. 서비스 시작
echo "4. 서비스 시작 중..."

# 백엔드 시작
cd /home/ubuntu/excel-project/backend
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Nginx 시작
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "=== 배포 완료 ==="
echo "서비스 상태 확인:"
echo "- 백엔드: pm2 status"
echo "- Nginx: sudo systemctl status nginx"
echo "- 웹사이트: http://your-ec2-ip"
echo ""
echo "로그 확인:"
echo "- 백엔드 로그: pm2 logs excel-project-backend"
echo "- Nginx 로그: sudo tail -f /var/log/nginx/excel-project.error.log" 