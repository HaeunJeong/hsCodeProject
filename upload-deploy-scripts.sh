#!/bin/bash

echo "📦 배포 스크립트 Git 저장소 업로드"
echo "=================================="

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 배포 관련 파일들 추가
echo -e "${YELLOW}배포 스크립트 파일들을 Git에 추가합니다...${NC}"

git add deploy-from-git.sh
git add setup-env.sh
git add setup-webhook.sh
git add quick-deploy.sh
git add webhook-server.js
git add webhook-package.json
git add webhook-ecosystem.config.js
git add nginx.conf
git add GIT_DEPLOYMENT_GUIDE.md

# 기존 Ubuntu 배포 스크립트들도 추가
git add deploy-setup.sh
git add backend/deploy.sh
git add frontend/deploy.sh
git add deploy-all.sh
git add update.sh
git add setup-ssl.sh
git add DEPLOYMENT_GUIDE.md

# Amazon Linux 배포 스크립트들도 추가
git add deploy-setup-amazon-linux.sh
git add backend/deploy-amazon-linux.sh
git add frontend/deploy-amazon-linux.sh
git add deploy-all-amazon-linux.sh
git add nginx-amazon-linux.conf
git add update-amazon-linux.sh
git add AMAZON_LINUX_DEPLOYMENT_GUIDE.md

echo -e "${GREEN}✅ 모든 배포 스크립트가 추가되었습니다.${NC}"

# 커밋 메시지 작성
echo -e "${YELLOW}커밋 메시지를 작성합니다...${NC}"
git commit -m "feat: add comprehensive deployment scripts

- Add Git-based auto-deployment system
- Add GitHub webhook server for auto-deployment
- Add quick deployment script for easy setup
- Add environment variable management
- Add deployment guides for Ubuntu and Amazon Linux
- Add SSL setup scripts
- Add update and maintenance scripts

Features:
- 🚀 One-command deployment setup
- 🔗 GitHub webhook integration
- 🔐 Secure environment variable management
- 📚 Comprehensive deployment guides
- 🛠️ Easy maintenance and updates
- 🌐 SSL certificate support
- 📊 PM2 process management

Deployment targets:
- Ubuntu 20.04/22.04
- Amazon Linux 2
- AWS EC2 with RDS PostgreSQL"

echo -e "${GREEN}✅ 커밋이 완료되었습니다.${NC}"

# 푸시
echo -e "${YELLOW}Git 저장소에 푸시합니다...${NC}"
git push origin main

echo -e "${GREEN}🎉 배포 스크립트가 성공적으로 업로드되었습니다!${NC}"
echo ""
echo -e "${YELLOW}📋 다음 단계:${NC}"
echo "1. AWS EC2 서버에 SSH 접속"
echo "2. 다음 명령어로 빠른 배포 실행:"
echo "   curl -sSL https://raw.githubusercontent.com/your-username/excel-project/main/quick-deploy.sh | bash"
echo ""
echo -e "${GREEN}🌐 서버에서 실행할 명령어:${NC}"
echo "wget https://raw.githubusercontent.com/your-username/excel-project/main/quick-deploy.sh"
echo "chmod +x quick-deploy.sh"
echo "./quick-deploy.sh" 