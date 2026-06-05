# Task Manager API – CI/CD Pipeline with Jenkins, Docker & GitHub

## Overview

This project demonstrates a complete CI/CD pipeline for a Django REST API using:

* Django REST Framework
* Docker
* Jenkins
* GitHub Webhooks
* Docker Hub
* SSH Deployment
* Ubuntu Linux

The pipeline automatically:

1. Pulls code from GitHub
2. Installs dependencies
3. Runs automated tests
4. Builds a Docker image
5. Pushes the image to Docker Hub
6. Connects to a remote server via SSH
7. Pulls the latest image
8. Deploys the application container
9. Performs a health check

---

# Architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    | Webhook
    v
Jenkins Server
    |
    | Build & Test
    v
Docker Hub
    |
    | Pull Latest Image
    v
Target Server (Ubuntu)
    |
    v
Docker Container
    |
    v
Django REST API
```

---

# Project Structure

```text
task-manager-api/
├── Jenkinsfile
├── Dockerfile
├── requirements.txt
├── manage.py
├── taskmanager/
├── tasks/
└── README.md
```

---

# Application Endpoints

## Health Check

```http
GET /api/health/
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Tasks API

```http
GET /api/tasks/
POST /api/tasks/
PUT /api/tasks/{id}/
DELETE /api/tasks/{id}/
```

---

# Jenkins Server Requirements

## Operating System

Ubuntu 22.04 or Ubuntu 24.04

---

## Install Java

Jenkins requires Java.

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
```

Verify:

```bash
java -version
```

---

## Install Jenkins

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key \
| sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/ \
| sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins -y
```

Start Jenkins:

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

Verify:

```bash
sudo systemctl status jenkins
```

---

## Install Docker

```bash
sudo apt install docker.io -y
```

Start Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Verify:

```bash
docker --version
```

---

## Allow Jenkins to Use Docker

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

Verify:

```bash
sudo -u jenkins docker ps
```

---

# Target Server Requirements

## Operating System

Ubuntu 22.04 or Ubuntu 24.04

---

## Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

Enable Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

---

# Create Deployment User

Create a dedicated deployment account.

```bash
sudo adduser deploy
```

Add to Docker group:

```bash
sudo usermod -aG docker deploy
```

Verify:

```bash
groups deploy
```

Expected output:

```text
deploy docker
```

---

# SSH Configuration

## Generate SSH Key on Jenkins Server

Switch to Jenkins user:

```bash
sudo su - jenkins
```

Generate key:

```bash
ssh-keygen -t rsa -b 4096
```

Press Enter for all prompts.

View public key:

```bash
cat ~/.ssh/id_rsa.pub
```

Copy the output.

---

## Configure Authorized Keys on Target Server

Switch to deploy user:

```bash
su - deploy
```

Create SSH directory:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Create authorized keys file:

```bash
nano ~/.ssh/authorized_keys
```

Paste Jenkins public key.

Set permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Verify:

```bash
ls -la ~/.ssh
```

Expected:

```text
drwx------ .ssh
-rw------- authorized_keys
```

---

## Test SSH Connectivity

From Jenkins server:

```bash
ssh deploy@TARGET_SERVER_IP
```

Successful login confirms SSH trust is working.

---

# Docker Hub Configuration

## Create Repository

Example:

```text
yourdockerhubusername/task-manager-api
```

---

## Create Access Token

Docker Hub:

```text
Account Settings
→ Security
→ Access Tokens
```

Create token and save it.

---

# Jenkins Plugins

Install the following plugins:

## Required Plugins

* Git Plugin
* Pipeline Plugin
* Docker Pipeline
* SSH Agent Plugin
* Credentials Binding Plugin
* GitHub Plugin
* GitHub Integration Plugin

Restart Jenkins after installation.

---

# Jenkins Credentials

## 1. GitHub Credential

Type:

```text
Username with password
```

ID:

```text
github_cred
```

Purpose:

```text
Clone repository from GitHub
```

---

## 2. Docker Hub Credential

Type:

```text
Username with password
```

ID:

```text
dockerhub
```

Purpose:

```text
Push Docker images
```

---

## 3. Deployment Server Credential

Type:

```text
SSH Username with private key
```

Username:

```text
deploy
```

ID:

```text
deploy-server
```

Purpose:

```text
SSH deployment to target server
```

---

# GitHub Webhook Configuration

Repository:

```text
Settings
→ Webhooks
→ Add Webhook
```

Payload URL:

```text
http://JENKINS_IP:8080/github-webhook/
```

Content Type:

```text
application/json
```

Events:

```text
Just the push event
```

Save webhook.

---

# Jenkins Pipeline Stages

## Checkout

Pull source code from GitHub.

## Install Dependencies

Install Python dependencies.

## Run Tests

Execute Django tests.

```bash
python manage.py test
```

## Build Docker Image

Build container image.

```bash
docker build -t task-manager-api .
```

## Push Image

Push image to Docker Hub.

```bash
docker push yourdockerhubusername/task-manager-api:latest
```

## Deploy

SSH into target server and deploy latest image.

## Health Check

Validate deployment.

```bash
curl http://TARGET_SERVER_IP:2020/api/health/
```

---

# Deployment Verification

Verify container:

```bash
docker ps
```

Verify image:

```bash
docker images
```

Verify endpoint:

```bash
curl http://TARGET_SERVER_IP:2020/api/health/
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# Skills Demonstrated

* CI/CD Pipeline Design
* Jenkins Administration
* GitHub Webhooks
* Docker Containerization
* Docker Hub Registry Management
* SSH Key Authentication
* Linux Server Administration
* Automated Testing
* Continuous Deployment
* Django REST API Development
* Infrastructure Automation

---

# Author

Sadiq Abdulrahman

Technical Operations Engineer | DevOps Enthusiast
