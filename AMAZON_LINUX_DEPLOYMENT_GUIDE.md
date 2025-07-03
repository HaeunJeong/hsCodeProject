# HAEBOM HS코드 자동분류 시스템 AWS EC2 배포 가이드 (Amazon Linux 2)

## SSH 접속 문제 해결

### 1. SSH 키 파일 권한 설정
```bash
chmod 400 ~/Downloads/haebom.pem
```

### 2. SSH 접속 명령어
```bash
ssh -i ~/Downloads/haebom.pem ec2-user@ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com
```

### 3. 접속 문제 해결
- **Permission denied 오류**: 키 파일 권한을 400으로 설정
- **사용자명 확인**: Amazon Linux는 `ec2-user` 사용
- **키 파일 경로**: `~/Downloads/haebom.pem` 사용

## 배포 단계

### 1단계: 프로젝트 파일 업로드
```bash
# 로컬에서 EC2로 파일 전송
scp -i ~/Downloads/haebom.pem -r excel-project ec2-user@ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com:/home/ec2-user/
```

### 2단계: 서버 접속 및 기본 설정
```bash
# EC2 인스턴스 접속
ssh -i ~/Downloads/haebom.pem ec2-user@ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com

# 기본 설정 스크립트 실행
cd /home/ec2-user/excel-project
chmod +x deploy-setup-amazon-linux.sh
./deploy-setup-amazon-linux.sh
```

### 3단계: 환경 변수 설정
```bash
# 백엔드 환경 변수 설정
cd /home/ec2-user/excel-project/backend
nano .env

# 다음 내용으로 수정:
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
```

### 4단계: 일괄 배포 실행
```bash
# 모든 스크립트 실행 권한 부여
chmod +x deploy-all-amazon-linux.sh
chmod +x backend/deploy-amazon-linux.sh
chmod +x frontend/deploy-amazon-linux.sh

# 일괄 배포 실행
./deploy-all-amazon-linux.sh
```

### 5단계: 서비스 상태 확인
```bash
# 백엔드 상태 확인
pm2 status

# Nginx 상태 확인
sudo systemctl status nginx

# 웹사이트 접속 테스트
curl http://ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com
```

## 주요 차이점 (Amazon Linux 2 vs Ubuntu)

### 패키지 관리자
- **Amazon Linux**: `yum` 사용
- **Ubuntu**: `apt` 사용

### 기본 사용자
- **Amazon Linux**: `ec2-user`
- **Ubuntu**: `ubuntu`

### Nginx 사용자
- **Amazon Linux**: `nginx`
- **Ubuntu**: `www-data`

### 패키지 설치 명령어
```bash
# Amazon Linux 2 전용
sudo yum update -y
sudo yum install -y python3 python3-pip
sudo amazon-linux-extras install -y nginx1
```

## 업데이트 방법

코드를 수정한 후 다음 명령어로 업데이트할 수 있습니다:
```bash
# 프로젝트 파일 업데이트
scp -i ~/Downloads/haebom.pem -r excel-project ec2-user@ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com:/home/ec2-user/

# 또는 Git 사용
cd /home/ec2-user/excel-project
git pull origin main

# 업데이트 스크립트 실행
chmod +x update-amazon-linux.sh
./update-amazon-linux.sh
```

## 문제 해결

### 로그 확인
```bash
# 백엔드 로그
pm2 logs excel-project-backend

# Nginx 로그
sudo tail -f /var/log/nginx/error.log

# 시스템 로그
sudo journalctl -u nginx
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

## 보안 설정

### 1. 방화벽 설정 (Amazon Linux 2)
```bash
# firewalld 설정
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### 2. 시스템 업데이트
```bash
# 시스템 업데이트
sudo yum update -y

# 보안 업데이트만
sudo yum update -y --security
```

## 웹사이트 접속

배포 완료 후 다음 URL로 접속할 수 있습니다:
- **웹사이트**: http://ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com
- **API 문서**: http://ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com/docs

## 주의사항

1. **SSH 키 파일 보안**: `haebom.pem` 파일을 안전하게 관리
2. **환경 변수**: `.env` 파일에 민감한 정보 포함
3. **포트 8000**: 배포 후 보안 그룹에서 제한 고려
4. **정기 업데이트**: 시스템 및 패키지 정기 업데이트 필요 