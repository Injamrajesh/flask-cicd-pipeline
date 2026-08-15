pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice'
        IMAGE_TAG = "${env.GIT_COMMIT}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %ECR_REPO%:%IMAGE_TAG% .'
            }
        }

        stage('Push Image to ECR') {
            steps {
                bat '''
                    aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %ECR_REPO%
                    docker push %ECR_REPO%:%IMAGE_TAG%
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'EC2 deployment will be configured next.'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed!'
        }
    }
}