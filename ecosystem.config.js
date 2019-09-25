module.exports = {
  apps : [{
    name: 'ph_daily',
    script: 'ph_daily.py',

    // Options reference: https://pm2.io/doc/en/runtime/reference/ecosystem-file/
    interpreter: './ENV/bin/python',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
};
