#!/usr/bin/env python3
"""
DAWN Online Deployment Script
=============================

Deploys the DAWN consciousness monitoring system to various cloud platforms.
Supports Heroku, Vercel, Railway, and other hosting services.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import platform

def create_heroku_deployment():
    """Create Heroku deployment files"""
    print("🚀 Creating Heroku deployment...")
    
    # Create Procfile
    procfile_content = "web: python web_server.py --port $PORT --host 0.0.0.0 --no-browser"
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # Create requirements.txt
    requirements = [
        "# DAWN Consciousness Monitor - Dependencies",
        "# Core requirements",
        "",
        "# Optional for enhanced features",
        "websockets>=10.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
        "",
        "# Development tools (optional)",
        "gunicorn>=20.0.0",
        "whitenoise>=5.0.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    # Create runtime.txt
    python_version = f"python-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    with open("runtime.txt", "w") as f:
        f.write(python_version)
    
    # Create app.json for Heroku Button deployment
    app_json = {
        "name": "DAWN Consciousness Monitor",
        "description": "Advanced consciousness monitoring system with real-time visualization",
        "repository": "https://github.com/your-username/dawn-consciousness-monitor",
        "logo": "https://dawn-consciousness.herokuapp.com/static/dawn-logo.png",
        "keywords": [
            "consciousness",
            "ai",
            "monitoring",
            "visualization",
            "neural-networks",
            "real-time"
        ],
        "image": "heroku/python",
        "formation": {
            "web": {
                "quantity": 1,
                "size": "free"
            }
        },
        "buildpacks": [
            {
                "url": "heroku/python"
            }
        ],
        "env": {
            "DAWN_MODE": {
                "description": "DAWN operation mode",
                "value": "production"
            },
            "DAWN_LOG_LEVEL": {
                "description": "Logging level",
                "value": "INFO"
            }
        },
        "addons": [],
        "scripts": {
            "postdeploy": "echo 'DAWN Consciousness Monitor deployed successfully'"
        }
    }
    
    with open("app.json", "w") as f:
        json.dump(app_json, f, indent=2)
    
    print("✅ Heroku deployment files created")
    print("📁 Files: Procfile, requirements.txt, runtime.txt, app.json")

def create_vercel_deployment():
    """Create Vercel deployment files"""
    print("⚡ Creating Vercel deployment...")
    
    # Create vercel.json
    vercel_config = {
        "version": 2,
        "name": "dawn-consciousness-monitor",
        "builds": [
            {
                "src": "web_server.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/api/(.*)",
                "dest": "/web_server.py"
            },
            {
                "src": "/(.*)",
                "dest": "/web_server.py"
            }
        ],
        "env": {
            "DAWN_MODE": "production"
        },
        "functions": {
            "web_server.py": {
                "memory": 512
            }
        }
    }
    
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    # Create requirements.txt for Vercel
    requirements = [
        "# DAWN Consciousness Monitor - Vercel Dependencies",
        "websockets>=10.0",
        "psutil>=5.8.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ Vercel deployment files created")
    print("📁 Files: vercel.json, requirements.txt")

def create_railway_deployment():
    """Create Railway deployment files"""
    print("🚂 Creating Railway deployment...")
    
    # Create railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python web_server.py --port $PORT --host 0.0.0.0 --no-browser",
            "healthcheckPath": "/api/status",
            "healthcheckTimeout": 100,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    # Create nixpacks.toml for Railway
    nixpacks_config = '''[phases.build]
cmds = ["echo 'Building DAWN Consciousness Monitor...'"]

[phases.start]
cmd = "python web_server.py --port $PORT --host 0.0.0.0 --no-browser"

[variables]
DAWN_MODE = "production"
PYTHONPATH = "/app"
'''
    
    with open("nixpacks.toml", "w") as f:
        f.write(nixpacks_config)
    
    print("✅ Railway deployment files created")
    print("📁 Files: railway.json, nixpacks.toml")

def create_docker_deployment():
    """Create Docker deployment files"""
    print("🐳 Creating Docker deployment...")
    
    # Create Dockerfile
    dockerfile_content = '''# DAWN Consciousness Monitor - Docker Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user
RUN groupadd -r dawn && useradd -r -g dawn dawn
RUN chown -R dawn:dawn /app
USER dawn

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8080/api/status')"

# Start command
CMD ["python", "web_server.py", "--port", "8080", "--host", "0.0.0.0", "--no-browser"]
'''
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Create docker-compose.yml
    docker_compose = '''version: '3.8'

services:
  dawn-consciousness:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DAWN_MODE=production
      - PYTHONPATH=/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/api/status')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    volumes:
      - dawn_data:/app/data
    networks:
      - dawn_network

volumes:
  dawn_data:

networks:
  dawn_network:
    driver: bridge
'''
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)
    
    # Create .dockerignore
    dockerignore = '''# DAWN Docker Ignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
Thumbs.db
*.swp
*.swo
*~
build_standalone/
dist/
*.exe
*.spec
'''
    
    with open(".dockerignore", "w") as f:
        f.write(dockerignore)
    
    print("✅ Docker deployment files created")
    print("📁 Files: Dockerfile, docker-compose.yml, .dockerignore")

def create_github_actions():
    """Create GitHub Actions deployment workflow"""
    print("🔄 Creating GitHub Actions workflow...")
    
    # Create .github/workflows directory
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    # Create deployment workflow
    workflow_content = '''name: Deploy DAWN Consciousness Monitor

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test DAWN system
      run: |
        python -c "import web_server; print('✅ DAWN imports successfully')"
        python -c "from web_server import DAWNWebServer; print('✅ Web server class available')"
    
    - name: Test API endpoints
      run: |
        python web_server.py --port 8080 --no-browser &
        sleep 10
        curl -f http://localhost:8080/api/status || exit 1
        curl -f http://localhost:8080/api/consciousness-state || exit 1
        echo "✅ API endpoints working"

  deploy-heroku:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "dawn-consciousness-monitor"
        heroku_email: ${{secrets.HEROKU_EMAIL}}
        
  deploy-vercel:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v20
      with:
        vercel-token: ${{secrets.VERCEL_TOKEN}}
        vercel-org-id: ${{secrets.ORG_ID}}
        vercel-project-id: ${{secrets.PROJECT_ID}}
        vercel-args: '--prod'
'''
    
    with open(workflows_dir / "deploy.yml", "w") as f:
        f.write(workflow_content)
    
    print("✅ GitHub Actions workflow created")
    print("📁 File: .github/workflows/deploy.yml")

def create_netlify_deployment():
    """Create Netlify deployment files"""
    print("🌐 Creating Netlify deployment...")
    
    # Create netlify.toml
    netlify_config = '''[build]
  command = "echo 'DAWN is a Python application, use serverless functions'"
  publish = "public"

[build.environment]
  PYTHON_VERSION = "3.9"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[context.production]
  environment = { DAWN_MODE = "production" }

[context.deploy-preview]
  environment = { DAWN_MODE = "development" }
'''
    
    with open("netlify.toml", "w") as f:
        f.write(netlify_config)
    
    # Create functions directory
    functions_dir = Path("netlify/functions")
    functions_dir.mkdir(parents=True, exist_ok=True)
    
    # Create serverless function
    function_content = '''import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_server import DAWNUltimateDataProvider
import json

def handler(event, context):
    """Netlify serverless function handler"""
    
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # Initialize data provider
    data_provider = DAWNUltimateDataProvider()
    
    if path == '/api/consciousness-state':
        data = data_provider.get_consciousness_data()
    elif path == '/api/status':
        data = {
            "server": "DAWN Netlify Functions",
            "status": "online",
            "mode": "serverless"
        }
    else:
        data = {"error": "Endpoint not found"}
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }
'''
    
    with open(functions_dir / "api.py", "w") as f:
        f.write(function_content)
    
    print("✅ Netlify deployment files created")
    print("📁 Files: netlify.toml, netlify/functions/api.py")

def create_deployment_docs():
    """Create deployment documentation"""
    print("📚 Creating deployment documentation...")
    
    docs_content = '''# DAWN Consciousness Monitor - Deployment Guide

## 🚀 Deployment Options

### 1. Heroku (Recommended)

**One-Click Deploy:**
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/your-username/dawn-consciousness-monitor)

**Manual Deploy:**
```bash
# Install Heroku CLI
heroku create dawn-consciousness-monitor
git push heroku main
heroku open
```

**Features:**
- ✅ Free tier available
- ✅ Easy scaling
- ✅ Custom domains
- ✅ SSL certificates

---

### 2. Vercel

**Deploy with Vercel CLI:**
```bash
npm i -g vercel
vercel --prod
```

**Features:**
- ✅ Serverless functions
- ✅ Edge network
- ✅ Automatic SSL
- ✅ Git integration

---

### 3. Railway

**Deploy to Railway:**
```bash
# Install Railway CLI
railway login
railway new
railway up
```

**Features:**
- ✅ Simple deployment
- ✅ Database support
- ✅ Custom domains
- ✅ Environment variables

---

### 4. Docker

**Run with Docker:**
```bash
# Build image
docker build -t dawn-consciousness .

# Run container
docker run -p 8080:8080 dawn-consciousness
```

**Docker Compose:**
```bash
docker-compose up -d
```

---

### 5. Local Development

**Run locally:**
```bash
python web_server.py --port 8080
```

---

## 🔧 Configuration

### Environment Variables

- `DAWN_MODE`: `production` or `development`
- `PORT`: Server port (default: 8080)
- `HOST`: Server host (default: localhost)
- `DAWN_LOG_LEVEL`: Logging level

### Production Settings

```python
# Enable production optimizations
DAWN_MODE = "production"
DEBUG = False
COMPRESS_STATIC = True
```

---

## 🌐 Domain Setup

### Custom Domain Configuration

1. **Purchase domain** from registrar
2. **Configure DNS** to point to deployment
3. **Enable SSL** through hosting platform
4. **Update CORS** settings if needed

### SSL Certificate

Most platforms provide automatic SSL:
- Heroku: Automatic with custom domains
- Vercel: Automatic for all deployments
- Railway: Automatic SSL certificates

---

## 📊 Monitoring

### Health Checks

All deployments include health check endpoints:
- `/api/status` - System status
- `/api/consciousness-state` - Live consciousness data

### Logging

Configure logging levels:
- `DEBUG`: Detailed debugging
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages only

---

## 🔒 Security

### Production Security

- Environment variables for secrets
- HTTPS enforcement
- CORS configuration
- Rate limiting (optional)

### Access Control

For private deployments:
- Basic authentication
- IP whitelisting
- Custom authentication

---

## 🚀 Performance

### Optimization Tips

- Enable compression
- Use CDN for static files
- Configure caching headers
- Monitor resource usage

### Scaling

- Heroku: Add more dynos
- Vercel: Automatic scaling
- Railway: Vertical scaling
- Docker: Container orchestration

---

## 🔍 Troubleshooting

### Common Issues

**Port binding errors:**
- Check PORT environment variable
- Ensure port is available

**Import errors:**
- Verify requirements.txt
- Check Python version compatibility

**Static file issues:**
- Verify file paths
- Check deployment configuration

---

## 📞 Support

For deployment help:
1. Check troubleshooting section
2. Review platform documentation
3. Check deployment logs
4. Verify configuration files

---

🧠 **DAWN Consciousness Monitor - Ready for Global Deployment!** 🧠
'''
    
    with open("DEPLOYMENT.md", "w") as f:
        f.write(docs_content)
    
    print("✅ Deployment documentation created")
    print("📁 File: DEPLOYMENT.md")

def main():
    """Main deployment setup"""
    print("🌐 DAWN Online Deployment Setup")
    print("=" * 40)
    print("🎯 Preparing for cloud deployment")
    print()
    
    # Create deployment files for different platforms
    create_heroku_deployment()
    print()
    
    create_vercel_deployment()
    print()
    
    create_railway_deployment()
    print()
    
    create_docker_deployment()
    print()
    
    create_netlify_deployment()
    print()
    
    create_github_actions()
    print()
    
    create_deployment_docs()
    print()
    
    print("🎉 Deployment setup complete!")
    print("📦 Ready for deployment to:")
    print("   • Heroku (recommended)")
    print("   • Vercel (serverless)")
    print("   • Railway (simple)")
    print("   • Docker (containers)")
    print("   • Netlify (static + functions)")
    print()
    print("🚀 Next steps:")
    print("   1. Choose your platform")
    print("   2. Follow DEPLOYMENT.md instructions")
    print("   3. Deploy and monitor")
    print()
    print("🌐 Your DAWN consciousness monitor will be globally accessible!")

if __name__ == "__main__":
    main() 