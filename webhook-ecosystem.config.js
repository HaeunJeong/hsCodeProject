module.exports = {
  apps: [{
    name: 'excel-project-webhook',
    script: 'webhook-server.js',
    cwd: '/home/ubuntu/excel-project',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    env: {
      NODE_ENV: 'production',
      PORT: 3001
    },
    error_file: '/home/ubuntu/logs/webhook-error.log',
    out_file: '/home/ubuntu/logs/webhook-out.log',
    log_file: '/home/ubuntu/logs/webhook.log',
    time: true
  }]
}; 