# HAEBOM HS코드 자동분류 시스템 AWS EC2 배포 가이드

## 사전 준비사항

### 1. AWS RDS PostgreSQL 설정
- 엔드포인트, 포트, 사용자명, 비밀번호, 데이터베이스명 확인
- 보안 그룹에서 EC2 인스턴스에서 접근 가능하도록 설정

### 2. EC2 인스턴스 생성
- AMI: Ubuntu 20.04 LTS 또는 Amazon Linux 2
- 인스턴스 타입: t3.small 이상 (최소 2GB RAM)
- 보안 그룹 설정:
  - SSH (22): 내 IP
  - HTTP (80): 0.0.0.0/0
  - HTTPS (443): 0.0.0.0/0
  - Custom TCP (8000): 0.0.0.0/0 (임시)

## 배포 단계

### 1단계: 서버 기본 설정
```bash
# EC2 인스턴스에 SSH 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 배포 스크립트 실행
chmod +x deploy-setup.sh
./deploy-setup.sh
```

### 2단계: 프로젝트 파일 업로드
```bash
# 로컬에서 프로젝트 파일을 EC2로 전송
scp -i your-key.pem -r excel-project ubuntu@your-ec2-ip:/home/ubuntu/

# 또는 Git 사용
cd /home/ubuntu
git clone https://github.com/your-username/excel-project.git
```

### 3단계: 환경 변수 설정
```bash
# 백엔드 환경 변수 설정
cd /home/ubuntu/excel-project/backend
nano .env

# 다음 내용으로 수정:
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
```

### 4단계: Nginx 설정 수정
```bash
# Nginx 설정 파일 수정
cd /home/ubuntu/excel-project
nano nginx.conf

# server_name을 EC2 IP 또는 도메인으로 수정
server_name your-ec2-ip;  # 또는 your-domain.com
```

### 5단계: 일괄 배포 실행
```bash
# 모든 스크립트 실행 권한 부여
chmod +x deploy-all.sh
chmod +x backend/deploy.sh
chmod +x frontend/deploy.sh

# 일괄 배포 실행
./deploy-all.sh
```

### 6단계: 서비스 상태 확인
```bash
# 백엔드 상태 확인
pm2 status

# Nginx 상태 확인
sudo systemctl status nginx

# 웹사이트 접속 테스트
curl http://your-ec2-ip
```

## 업데이트 방법

코드를 수정한 후 다음 명령어로 업데이트할 수 있습니다:
```bash
# 프로젝트 파일 업데이트 (Git 사용 시)
cd /home/ubuntu/excel-project
git pull origin main

# 업데이트 스크립트 실행
chmod +x update.sh
./update.sh
```

## SSL 인증서 설정 (도메인 있는 경우)

도메인이 있는 경우 무료 SSL 인증서를 설정할 수 있습니다:
```bash
chmod +x setup-ssl.sh
./setup-ssl.sh your-domain.com
```

## 문제 해결

### 로그 확인
```bash
# 백엔드 로그
pm2 logs excel-project-backend

# Nginx 로그
sudo tail -f /var/log/nginx/excel-project.error.log
```

### 서비스 재시작
```bash
# 백엔드 재시작
pm2 restart excel-project-backend

# Nginx 재시작
sudo systemctl restart nginx
```

### 포트 확인
```bash
# 포트 8000 사용 확인
sudo netstat -tlnp | grep 8000

# 포트 80 사용 확인
sudo netstat -tlnp | grep 80
```

## 보안 설정 (배포 후)

### 1. 방화벽 설정
```bash
# UFW 활성화
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```

### 2. 포트 8000 접근 제한
```bash
# EC2 보안 그룹에서 포트 8000 규칙 삭제
# (Nginx 프록시를 통해서만 접근하도록)
```

### 3. 정기적인 시스템 업데이트
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# PM2 자동 시작 설정
pm2 startup
pm2 save
```

## 백업 및 모니터링

### 데이터베이스 백업
```bash
# 정기적인 데이터베이스 백업 스크립트 생성
pg_dump -h your-rds-endpoint -U username -d dbname > backup_$(date +%Y%m%d).sql
```

### 모니터링 도구
- PM2 모니터링: `pm2 monit`
- 시스템 리소스: `htop`
- 디스크 사용량: `df -h`

## 주의사항

1. 환경 변수 파일(.env)에는 민감한 정보가 포함되어 있으니 권한 관리에 주의
2. 정기적으로 시스템 업데이트 및 보안 패치 적용
3. 백업 정책 수립 및 정기적인 백업 실행
4. 로그 파일 관리 (로그 로테이션 설정)
5. SSL 인증서 자동 갱신 확인 (Let's Encrypt 사용 시) 