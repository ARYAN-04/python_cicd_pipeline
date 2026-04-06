# Python CI/CD Pipeline

A production-ready Flask API with automated CI/CD pipeline, containerization, and security scanning.

[![CI/CD Pipeline](https://github.com/ARYAN-04/python_cicd_pipeline/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ARYAN-04/python_cicd_pipeline/actions/workflows/ci-cd.yml)
[![Docker Hub](https://img.shields.io/docker/v/rn208/flask-api?sort=semver&logo=docker)](https://hub.docker.com/r/rn208/flask-api)

## How It Works

This project implements a 5-phase CI/CD pipeline that automatically builds, tests, and deploys a Flask API to Docker Hub with security scanning.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CI/CD Pipeline                                │
├─────────────┬─────────────┬────────────────┬─────────────┬─────────┤
│  Phase 1    │  Phase 2    │    Phase 3     │   Phase 4   │ Phase 5 │
│  Code       │  Container  │    GitHub      │  Security   │  Deploy │
│  & Tests    │  Build      │    Actions     │  Scan       │  & Docs │
└─────────────┴─────────────┴────────────────┴─────────────┴─────────┘
```

### Phase Breakdown

#### Phase 1: Code & Tests
- **Flask API** with `/health` and `/add` endpoints
- **Pytest** test suite with 80% code coverage requirement
- **Separated dependencies**: Production (`requirements.txt`) vs Development (`requirements-dev.txt`)

#### Phase 2: Container Build
- **Multi-stage Dockerfile** for optimized image size
- **Builder stage**: Runs tests during build (fail-fast)
- **Production stage**: Lean image with runtime dependencies only
- **Security**: Non-root user (`appuser`) for container isolation

#### Phase 3: CI/CD Automation
- **GitHub Actions** workflow with 3 sequential jobs
- **lint**: Code quality checks with flake8
- **test**: Pytest with 80% coverage gate
- **build-and-push**: Docker image to Hub with `latest` + commit SHA tags

#### Phase 4: Security Scanning
- **Trivy** vulnerability scanner on pushed images
- **CRITICAL/ HIGH severity detection**
- **SARIF reporting** to GitHub Security tab
- **Pipeline fails** on critical vulnerabilities

#### Phase 5: Documentation & Deployment
- **Docker Hub** for container hosting
- **GitHub Actions badges** for visibility
- **Usage instructions** for easy deployment

### Workflow Triggers

| Trigger | Jobs Run |
|---------|----------|
| Push to `main` | lint → test → build → scan |
| Pull Request to `main` | lint → test (no build) |

## Quick Start

### Pull the Image

```bash
docker pull rn208/flask-api:latest
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name flask-api rn208/flask-api:latest
```

### Test the API

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Addition Endpoint:**
```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'
```

### Stop and Remove

```bash
docker stop flask-api && docker rm flask-api
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_APP` | `app.py` | Flask application entry point |
| `FLASK_ENV` | `production` | Flask environment mode |

## Exposed Port

| Port | Protocol | Service |
|------|----------|---------|
| `5000` | HTTP | Flask API |

## Docker Compose (Optional)

```yaml
version: '3.8'
services:
  flask-api:
    image: rn208/flask-api:latest
    ports:
      - "5000:5000"
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```
