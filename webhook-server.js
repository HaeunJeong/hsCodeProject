const express = require('express');
const crypto = require('crypto');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

// GitHub webhook secret (보안을 위해 실제 값으로 변경 필요)
const WEBHOOK_SECRET = 'your-webhook-secret-here';

// 로그 함수
function log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}`;
    console.log(logMessage);
    
    // 로그 파일에도 기록
    const logFile = '/home/ubuntu/logs/webhook.log';
    fs.appendFileSync(logFile, logMessage + '\n');
}

// GitHub webhook 서명 검증
function verifySignature(req, res, next) {
    const signature = req.headers['x-hub-signature-256'];
    const payload = JSON.stringify(req.body);
    
    if (!signature) {
        return res.status(401).send('Missing signature');
    }

    const expectedSignature = `sha256=${crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(payload)
        .digest('hex')}`;

    if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))) {
        return res.status(401).send('Invalid signature');
    }

    next();
}

// 미들웨어 설정
app.use(express.json());

// 건강 상태 체크 엔드포인트
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK', timestamp: new Date().toISOString() });
});

// GitHub webhook 엔드포인트
app.post('/webhook', verifySignature, (req, res) => {
    const event = req.headers['x-github-event'];
    const payload = req.body;

    log(`Received ${event} event`);

    // push 이벤트만 처리
    if (event === 'push') {
        const branch = payload.ref.replace('refs/heads/', '');
        log(`Push to branch: ${branch}`);

        // main 브랜치에 대한 push만 배포
        if (branch === 'main' || branch === 'master') {
            log('Starting deployment...');
            
            // 배포 스크립트 실행
            const deployScript = '/home/ubuntu/excel-project/deploy-from-git.sh';
            
            exec(`chmod +x ${deployScript} && ${deployScript}`, (error, stdout, stderr) => {
                if (error) {
                    log(`Deployment error: ${error.message}`);
                    return res.status(500).send('Deployment failed');
                }
                
                if (stderr) {
                    log(`Deployment stderr: ${stderr}`);
                }
                
                log(`Deployment stdout: ${stdout}`);
                log('Deployment completed successfully');
                
                res.status(200).send('Deployment triggered successfully');
            });
        } else {
            log(`Ignoring push to branch: ${branch}`);
            res.status(200).send('Branch ignored');
        }
    } else {
        log(`Ignoring ${event} event`);
        res.status(200).send('Event ignored');
    }
});

// 서버 시작
app.listen(PORT, '0.0.0.0', () => {
    log(`Webhook server listening on port ${PORT}`);
});

// 예외 처리
process.on('uncaughtException', (error) => {
    log(`Uncaught Exception: ${error.message}`);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    log(`Unhandled Rejection at: ${promise}, reason: ${reason}`);
    process.exit(1);
}); 