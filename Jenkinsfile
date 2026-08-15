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
                
                    sh 'python3 -m pip install --break-system-packages -r requirements.txt'
                
            }
        }

        stage('Run Tests') {
            steps {
               withCredentials([string(credentialsId: 'mongo-uri', variable: 'MONGO_URI')]) {
            sh                 export MONGO_URI="$MONGO_URI"
                python3 -m pytest -v
            
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
                    docker push $ECR_REPO:$IMAGE_TAG
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