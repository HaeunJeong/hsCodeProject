#!/bin/bash

echo "=== SSL 인증서 설정 시작 ==="

# 도메인 확인
if [ -z "$1" ]; then
    echo "사용법: ./setup-ssl.sh your-domain.com"
    echo "예시: ./setup-ssl.sh haebom.com"
    exit 1
fi

DOMAIN=$1
echo "도메인: $DOMAIN"

# Certbot 설치
echo "1. Certbot 설치 중..."
sudo apt install -y certbot python3-certbot-nginx

# SSL 인증서 발급
echo "2. SSL 인증서 발급 중..."
sudo certbot --nginx -d $DOMAIN

# 자동 갱신 설정 확인
echo "3. 자동 갱신 설정 확인..."
sudo certbot renew --dry-run

echo "=== SSL 설정 완료 ==="
echo "웹사이트: https://$DOMAIN" 