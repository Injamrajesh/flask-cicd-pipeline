pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '310297108115.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = '310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice'
        IMAGE_TAG = "${env.GIT_COMMIT}"
    }

    stages {

        // ==============================
        // 1. Checkout Source Code
        // ==============================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ==============================
        // 2. Install Python Dependencies
        // ==============================
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        // ==============================
        // 3. Run Tests
        // ==============================
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

        // ==============================
        // 4. Build Docker Image
        // ==============================
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $ECR_REPO:$IMAGE_TAG .
                '''
            }
        }

        // ==============================
        // 5. Push Docker Image to ECR
        // ==============================
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

                        aws ecr get-login-password \
                            --region "$AWS_REGION" | \
                            docker login \
                            --username AWS \
                            --password-stdin "$ECR_REGISTRY"

                        echo "Pushing Docker image..."

                        docker push "$ECR_REPO:$IMAGE_TAG"

                        echo "Docker image pushed successfully."
                    '''
                }
            }
        }

        // ==============================
        // 6. Test SSH Connection to EC2
        // ==============================
        stage('Test EC2 SSH') {
            steps {
                sshagent(['flask-practice-ec2-ssh']) {
                    sh '''
                        set -e

                        echo "Testing SSH connection to EC2..."

                        ssh -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "echo SSH connection successful && hostname"

                        echo "SSH test completed successfully."
                    '''
                }
            }
        }

        // ==============================
        // 7. Deploy Docker Image to EC2
        // ==============================
        stage('Deploy to EC2') {
            steps {

                withCredentials([
                    string(
                        credentialsId: 'MONGO_URI_RI',
                        variable: 'MONGO_URI'
                    ),
                    string(
                        credentialsId: 'FLASK_SECRET_KEY',
                        variable: 'SECRET_KEY'
                    )
                ]) {

                    sshagent(['flask-practice-ec2-ssh']) {

                        sh '''
                            set -e

                            echo "======================================"
                            echo "Starting EC2 Deployment"
                            echo "======================================"

                            echo "Connecting to EC2..."

                            ssh -o StrictHostKeyChecking=no \
                                ec2-user@98.89.45.250 "
                                
                                set -e

                                echo 'Logging in to Amazon ECR...'

                                aws ecr get-login-password \
                                    --region us-east-1 | \
                                    docker login \
                                    --username AWS \
                                    --password-stdin \
                                    310297108115.dkr.ecr.us-east-1.amazonaws.com

                                echo 'Pulling new Docker image...'

                                docker pull \
                                    310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice:${IMAGE_TAG}

                                echo 'Stopping old container...'

                                docker stop flask-practice || true

                                echo 'Removing old container...'

                                docker rm flask-practice || true

                                echo 'Starting new container...'

                                docker run -d \
                                    --name flask-practice \
                                    -p 5000:5000 \
                                    -e MONGO_URI='${MONGO_URI}' \
                                    -e SECRET_KEY='${SECRET_KEY}' \
                                    310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice:${IMAGE_TAG}

                                echo 'Deployment completed successfully.'

                                echo 'Running containers:'

                                docker ps
                            "

                            echo "======================================"
                            echo "EC2 Deployment Finished"
                            echo "======================================"
                        '''
                    }
                }
            }
        }
    }

    // ==============================
    // Pipeline Result
    // ==============================
    post {

        success {
            echo '======================================'
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'CI/CD PIPELINE FAILED!'
            echo '======================================'
        }
    }
}