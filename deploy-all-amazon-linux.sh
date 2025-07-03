#!/bin/bash

echo "=== HAEBOM HS코드 자동분류 시스템 배포 시작 (Amazon Linux 2) ==="

# 1. Nginx 설정 파일 복사
echo "1. Nginx 설정 중..."
sudo cp nginx-amazon-linux.conf /etc/nginx/conf.d/excel-project.conf

# 기본 설정 파일 백업
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Nginx 설정 테스트
sudo nginx -t
if [ $? -ne 0 ]; then
    echo "Nginx 설정 오류가 있습니다. 설정을 확인해주세요."
    exit 1
fi

# 2. 백엔드 배포
echo "2. 백엔드 배포 중..."
cd /home/ec2-user/excel-project/backend
chmod +x deploy-amazon-linux.sh
./deploy-amazon-linux.sh

# 3. 프론트엔드 배포
echo "3. 프론트엔드 배포 중..."
cd /home/ec2-user/excel-project/frontend
chmod +x deploy-amazon-linux.sh
./deploy-amazon-linux.sh

# 4. 서비스 시작
echo "4. 서비스 시작 중..."

# 백엔드 시작
cd /home/ec2-user/excel-project/backend
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Nginx 시작
sudo systemctl start nginx
sudo systemctl enable nginx

echo "=== 배포 완료 ==="
echo "서비스 상태 확인:"
echo "- 백엔드: pm2 status"
echo "- Nginx: sudo systemctl status nginx"
echo "- 웹사이트: http://ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com"
echo ""
echo "로그 확인:"
echo "- 백엔드 로그: pm2 logs excel-project-backend"
echo "- Nginx 로그: sudo tail -f /var/log/nginx/error.log" 