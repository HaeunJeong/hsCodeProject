# Git 기반 자동 배포 시스템 설정 가이드

## 🎯 개요
Git push 시 자동으로 AWS EC2 서버에 배포되는 시스템을 구축하는 방법입니다.

## 📋 사전 준비사항
- ✅ EC2 인스턴스 실행 중 (Ubuntu, IP: 13.209.30.21)
- ✅ Git 저장소에 코드 업로드 완료
- ✅ .env 파일은 .gitignore에 추가됨
- ✅ SSH 접속 가능

## 🚀 1단계: 서버 초기 설정

### 1.1 Ubuntu 서버 접속
```bash
ssh -i ~/Downloads/haebom.pem ubuntu@13.209.30.21
```

### 1.2 기본 패키지 설치
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git unzip python3 python3-pip python3-venv nodejs npm nginx
sudo npm install -g pm2
```

## 🔧 2단계: 프로젝트 설정

### 2.1 프로젝트 파일 업로드
로컬에서 실행 (SCP 복사 완료 후 건너뛰기):
```bash
scp -i ~/Downloads/haebom.pem -r excel-project ubuntu@13.209.30.21:/home/ubuntu/
```

### 2.2 Git 저장소 URL 설정
**중요**: `deploy-from-git.sh` 파일에서 Git 저장소 URL을 실제 값으로 수정:
```bash
nano /home/ubuntu/excel-project/deploy-from-git.sh
# GIT_REPO="https://github.com/your-username/excel-project.git" 수정
```

### 2.3 환경 변수 설정
```bash
cd /home/ubuntu/excel-project
chmod +x setup-env.sh
./setup-env.sh

# .env 파일 수정
nano backend/.env
```

**필수 수정 사항**:
```env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname
SECRET_KEY=your-generated-secret-key
```

## 🎯 3단계: 최초 배포 실행

### 3.1 Git 기반 배포 실행
```bash
chmod +x deploy-from-git.sh
./deploy-from-git.sh
```

### 3.2 웹사이트 접속 확인
- **웹사이트**: http://13.209.30.21
- **API 문서**: http://13.209.30.21/docs

## 🔗 4단계: 자동 배포 시스템 구축

### 4.1 Webhook 서버 설정
```bash
chmod +x setup-webhook.sh
./setup-webhook.sh
```

**중요**: 출력되는 Webhook Secret을 기록해두세요!

### 4.2 AWS 보안 그룹 설정
AWS 콘솔에서 포트 3001 추가:
- **Type**: Custom TCP
- **Port**: 3001
- **Source**: 0.0.0.0/0

## 🐙 5단계: GitHub Webhook 설정

### 5.1 GitHub Repository 설정
1. **GitHub Repository → Settings → Webhooks**
2. **Add webhook** 클릭
3. 다음 정보 입력:
   - **Payload URL**: `http://13.209.30.21:3001/webhook`
   - **Content type**: `application/json`
   - **Secret**: 4.1에서 생성된 Webhook Secret
   - **Events**: "Just the push event" 선택
4. **Add webhook** 클릭

### 5.2 Webhook 테스트
```bash
# 로컬에서 테스트 push
git add .
git commit -m "test: webhook deployment"
git push origin main

# 서버에서 로그 확인
pm2 logs excel-project-webhook
```

## 🔄 6단계: 자동 배포 흐름

### 배포 프로세스
1. **로컬에서 코드 수정**
2. **Git commit & push**
3. **GitHub webhook 호출**
4. **서버에서 자동 배포 실행**
5. **웹사이트 업데이트 완료**

### 배포 상태 확인
```bash
# 서비스 상태 확인
pm2 status

# 로그 확인
pm2 logs excel-project-backend
pm2 logs excel-project-webhook

# 웹사이트 확인
curl http://13.209.30.21
```

## 🛠️ 7단계: 관리 명령어

### 서비스 관리
```bash
# 모든 서비스 재시작
pm2 restart all

# 개별 서비스 재시작
pm2 restart excel-project-backend
pm2 restart excel-project-webhook

# 로그 확인
pm2 logs
pm2 logs excel-project-backend
pm2 logs excel-project-webhook

# 서비스 중지
pm2 stop all
```

### 수동 배포 (필요시)
```bash
cd /home/ubuntu/excel-project
./deploy-from-git.sh
```

## 🚨 8단계: 문제 해결

### 일반적인 문제들

#### 1. Webhook이 동작하지 않는 경우
```bash
# 포트 3001 확인
sudo netstat -tlnp | grep 3001

# Webhook 서버 로그 확인
pm2 logs excel-project-webhook

# 서버 재시작
pm2 restart excel-project-webhook
```

#### 2. 배포 실패 시
```bash
# 배포 로그 확인
tail -f /home/ubuntu/logs/webhook.log

# 백엔드 로그 확인
pm2 logs excel-project-backend

# 수동 배포 시도
./deploy-from-git.sh
```

#### 3. 데이터베이스 연결 오류
```bash
# .env 파일 확인
cat backend/.env

# 데이터베이스 연결 테스트
cd backend
source venv/bin/activate
python -c "from app.core.database import engine; print('DB connection OK')"
```

## 📝 9단계: 보안 최적화

### 9.1 방화벽 설정
```bash
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3001
```

### 9.2 정기적인 업데이트
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# PM2 업데이트
npm update -g pm2
```

## 🎉 배포 완료!

이제 로컬에서 코드를 수정하고 `git push`만 하면 자동으로 서버에 배포됩니다!

### 접속 정보
- **웹사이트**: http://13.209.30.21
- **API 문서**: http://13.209.30.21/docs
- **Webhook 상태**: http://13.209.30.21:3001/health

### 배포 테스트
```bash
# 로컬에서 테스트
git add .
git commit -m "feat: add new feature"
git push origin main

# 약 1-2분 후 웹사이트 확인
curl http://13.209.30.21
``` 