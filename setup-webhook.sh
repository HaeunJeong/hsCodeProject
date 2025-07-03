#!/bin/bash

echo "=== Webhook 서버 설정 시작 ==="

# 프로젝트 디렉토리로 이동
cd /home/ubuntu/excel-project

# 1. Webhook 서버 의존성 설치
echo "1. Webhook 서버 의존성 설치 중..."
cp webhook-package.json package.json
npm install

# 2. 로그 디렉토리 생성
echo "2. 로그 디렉토리 생성 중..."
mkdir -p /home/ubuntu/logs

# 3. Webhook secret 설정
echo "3. Webhook secret 설정 중..."
WEBHOOK_SECRET=$(openssl rand -hex 32)
echo "생성된 Webhook Secret: $WEBHOOK_SECRET"
echo "이 값을 GitHub Repository Settings > Webhooks에서 사용하세요."

# webhook-server.js 파일의 secret 업데이트
sed -i "s/your-webhook-secret-here/$WEBHOOK_SECRET/g" webhook-server.js

# 4. PM2로 Webhook 서버 시작
echo "4. Webhook 서버 시작 중..."
pm2 start webhook-ecosystem.config.js

# 5. PM2 설정 저장
pm2 save

echo "=== Webhook 서버 설정 완료 ==="
echo ""
echo "📋 GitHub 설정 정보:"
echo "- Payload URL: http://13.209.30.21:3001/webhook"
echo "- Content type: application/json"
echo "- Secret: $WEBHOOK_SECRET"
echo "- Events: Just the push event"
echo ""
echo "🔧 서버 관리 명령어:"
echo "- 상태 확인: pm2 status"
echo "- 로그 확인: pm2 logs excel-project-webhook"
echo "- 서버 재시작: pm2 restart excel-project-webhook"
echo ""
echo "⚠️  보안 그룹에 포트 3001 추가 필요!"
echo "AWS 콘솔 → EC2 → Security Groups → 포트 3001 (TCP) 추가" 