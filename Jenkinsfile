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
// quick test to check if the application is working before running the full test suite
        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test
                '''
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    docker build -t $DOCKER_USER/task-manager-api:latest .

                    docker push $DOCKER_USER/task-manager-api:latest
                    '''
                }
            }
        }
// deploy the application to the server using SSH and Docker
        stage('Deploy') {
            steps {
                sshagent(['deploy-server']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no deploy@195.7.5.147 "
                        docker stop task-manager-api || true
                        docker rm task-manager-api || true

                        docker pull successtech/task-manager-api:latest

                        docker run -d \
                            --name task-manager-api \
                            -p 2020:8000 \
                            successtech/task-manager-api:latest
                    "
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                sshagent(['deploy-server']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no deploy@195.7.5.147 "
                        sleep 10
                        curl http://localhost:2020/api/health/
                    "
                    '''
                }
            }
        }
    }
}