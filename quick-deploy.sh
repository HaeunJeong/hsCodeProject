#!/bin/bash

echo "🚀 HAEBOM HS코드 자동분류 시스템 빠른 배포 시작"
echo "=================================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 오류 처리
set -e

# 필수 정보 확인
read -p "Git 저장소 URL을 입력하세요 (예: https://github.com/username/excel-project.git): " GIT_REPO
if [ -z "$GIT_REPO" ]; then
    echo -e "${RED}❌ Git 저장소 URL이 필요합니다!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git 저장소: $GIT_REPO${NC}"

# 1. 기본 패키지 설치
echo -e "${YELLOW}1. 기본 패키지 설치 중...${NC}"
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git unzip python3 python3-pip python3-venv nodejs npm nginx
sudo npm install -g pm2

# 2. 프로젝트 클론 (기존 디렉토리 있으면 제거)
echo -e "${YELLOW}2. 프로젝트 클론 중...${NC}"
cd /home/ubuntu
if [ -d "excel-project" ]; then
    rm -rf excel-project
fi
git clone $GIT_REPO excel-project
cd excel-project

# 3. Git 저장소 URL 업데이트
echo -e "${YELLOW}3. 배포 스크립트 설정 중...${NC}"
sed -i "s|https://github.com/your-username/excel-project.git|$GIT_REPO|g" deploy-from-git.sh

# 4. 환경 변수 설정
echo -e "${YELLOW}4. 환경 변수 설정 중...${NC}"
./setup-env.sh

# 5. 최초 배포 실행
echo -e "${YELLOW}5. 최초 배포 실행 중...${NC}"
chmod +x deploy-from-git.sh

echo -e "${RED}⚠️  중요: 환경 변수 설정이 필요합니다!${NC}"
echo -e "${YELLOW}다음 명령어로 .env 파일을 수정하세요:${NC}"
echo "nano backend/.env"
echo ""
echo -e "${YELLOW}수정 후 다음 명령어로 배포를 계속하세요:${NC}"
echo "./deploy-from-git.sh"
echo ""
echo -e "${GREEN}✅ 기본 설정이 완료되었습니다!${NC}"

# 6. Webhook 설정 (선택사항)
echo ""
read -p "GitHub Webhook 자동 배포를 설정하시겠습니까? (y/n): " SETUP_WEBHOOK

if [ "$SETUP_WEBHOOK" = "y" ] || [ "$SETUP_WEBHOOK" = "Y" ]; then
    echo -e "${YELLOW}6. Webhook 서버 설정 중...${NC}"
    chmod +x setup-webhook.sh
    ./setup-webhook.sh
    
    echo ""
    echo -e "${GREEN}🎉 모든 설정이 완료되었습니다!${NC}"
    echo ""
    echo -e "${YELLOW}📋 다음 단계:${NC}"
    echo "1. backend/.env 파일 수정"
    echo "2. 최초 배포 실행: ./deploy-from-git.sh"
    echo "3. GitHub에서 Webhook 설정"
    echo "4. 보안 그룹에 포트 3001 추가"
    echo ""
    echo -e "${GREEN}🌐 접속 정보:${NC}"
    echo "- 웹사이트: http://13.209.30.21"
    echo "- API 문서: http://13.209.30.21/docs"
    echo "- Webhook 상태: http://13.209.30.21:3001/health"
else
    echo -e "${GREEN}✅ 기본 배포 시스템이 준비되었습니다!${NC}"
    echo ""
    echo -e "${YELLOW}📋 다음 단계:${NC}"
    echo "1. backend/.env 파일 수정"
    echo "2. 최초 배포 실행: ./deploy-from-git.sh"
    echo ""
    echo -e "${GREEN}🌐 접속 정보:${NC}"
    echo "- 웹사이트: http://13.209.30.21"
    echo "- API 문서: http://13.209.30.21/docs"
fi

echo ""
echo -e "${GREEN}=================================================="
echo "🎉 HAEBOM HS코드 자동분류 시스템 배포 준비 완료!"
echo "==================================================${NC}" 