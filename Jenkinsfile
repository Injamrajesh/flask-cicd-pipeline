pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '310297108115.dkr.ecr.us-east-1.amazonaws.com'
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
                withCredentials([
                    string(
                        credentialsId: 'MONGO_URI_RI',
                        variable: 'MONGO_URI'
                    )
                ]) {
                    sh '''
                        python3 -m pytest -v
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
            }
        }

        stage('Push Image to ECR') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-ecr-credentials']
                ]) {
                    sh '''
                        set -e

                        echo "Checking AWS credentials..."
                        aws sts get-caller-identity

                        echo "Logging in to ECR..."
                        aws ecr get-login-password --region "$AWS_REGION" | \
                            docker login --username AWS --password-stdin "$ECR_REGISTRY"

                        echo "Pushing Docker image..."
                        docker push "$ECR_REPO:$IMAGE_TAG"
                    '''
                }
            }
        }

        stage('Test EC2 SSH') {
        steps {
        sshagent(credentials: ['flask-practice-ec2-ssh']) {
            sh '''
                ssh -o StrictHostKeyChecking=no ec2-user@98.89.45.250 \
                "echo SSH connection successful && hostname"
            '''
        }
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