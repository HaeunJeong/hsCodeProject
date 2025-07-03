#!/bin/bash

# Ubuntu 기준 설정 스크립트
echo "=== EC2 서버 기본 설정 시작 ==="

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y curl wget git unzip software-properties-common

# Python 3.9+ 설치
sudo apt install -y python3 python3-pip python3-venv

# Node.js 18 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Nginx 설치
sudo apt install -y nginx

# PM2 전역 설치 (프로세스 관리용)
sudo npm install -g pm2

# PostgreSQL 클라이언트 설치 (AWS RDS 연결용)
sudo apt install -y postgresql-client

echo "=== 기본 설정 완료 ==="

# 프로젝트 디렉토리 생성
mkdir -p /home/ubuntu/excel-project
cd /home/ubuntu/excel-project

echo "이제 프로젝트 파일을 업로드하거나 Git clone을 진행하세요." 