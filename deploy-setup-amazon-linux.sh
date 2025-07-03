#!/bin/bash

# Amazon Linux 2 기준 설정 스크립트
echo "=== EC2 서버 기본 설정 시작 (Amazon Linux 2) ==="

# 시스템 업데이트
sudo yum update -y

# 필수 패키지 설치
sudo yum install -y curl wget git unzip

# Python 3.9 설치
sudo yum install -y python3 python3-pip

# Python 가상환경 도구 설치
sudo pip3 install virtualenv

# Node.js 18 설치
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Nginx 설치
sudo amazon-linux-extras install -y nginx1

# PM2 전역 설치 (프로세스 관리용)
sudo npm install -g pm2

# PostgreSQL 클라이언트 설치 (AWS RDS 연결용)
sudo yum install -y postgresql

echo "=== 기본 설정 완료 ==="

# 프로젝트 디렉토리 생성
mkdir -p /home/ec2-user/excel-project
cd /home/ec2-user/excel-project

echo "이제 프로젝트 파일을 업로드하거나 Git clone을 진행하세요."
echo "업로드 명령어 예시:"
echo "scp -i ~/Downloads/haebom.pem -r excel-project ec2-user@ec2-43-201-30-128.ap-northeast-2.compute.amazonaws.com:/home/ec2-user/" 