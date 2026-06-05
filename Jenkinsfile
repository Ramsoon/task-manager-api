pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t task-manager-api:latest .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop task-manager-api || true
                docker rm task-manager-api || true

                docker run -d \
                    --name task-manager-api \
                    -p 8000:8000 \
                    task-manager-api:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 10
                curl http://localhost:8000/api/health/
                '''
            }
        }
    }
}