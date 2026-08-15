pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '310297108115.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = '310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice'
        IMAGE_TAG = "${env.GIT_COMMIT}"
    }

    stages {

        // ==========================================
        // 1. Checkout Source Code
        // ==========================================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ==========================================
        // 2. Install Dependencies
        // ==========================================
        stage('Install Dependencies') {
            steps {
                sh '''
                    set -e

                    echo "Installing Python dependencies..."

                    python3 -m pip install \
                        --break-system-packages \
                        -r requirements.txt

                    echo "Dependencies installed successfully."
                '''
            }
        }

        // ==========================================
        // 3. Run Tests
        // ==========================================
        stage('Run Tests') {
            steps {

                withCredentials([
                    string(
                        credentialsId: 'MONGO_URI_RI',
                        variable: 'MONGO_URI'
                    )
                ]) {

                    sh '''
                        set -e

                        echo "======================================"
                        echo "Running Application Tests"
                        echo "======================================"

                        if [ -z "$MONGO_URI" ]; then
                            echo "ERROR: MONGO_URI credential is empty."
                            exit 1
                        fi

                        python3 -m pytest -v

                        echo "======================================"
                        echo "Tests completed successfully."
                        echo "======================================"
                    '''
                }
            }
        }

        // ==========================================
        // 4. Build Docker Image
        // ==========================================
        stage('Build Docker Image') {
            steps {

                sh '''
                    set -e

                    echo "======================================"
                    echo "Building Docker Image"
                    echo "======================================"

                    docker build \
                        -t "$ECR_REPO:$IMAGE_TAG" \
                        .

                    echo "Docker image built successfully."
                '''
            }
        }

        // ==========================================
        // 5. Push Image to Amazon ECR
        // ==========================================
        stage('Push Image to ECR') {
            steps {

                withCredentials([
                    [
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-ecr-credentials'
                    ]
                ]) {

                    sh '''
                        set -e

                        echo "======================================"
                        echo "Checking AWS Credentials"
                        echo "======================================"

                        aws sts get-caller-identity

                        echo "======================================"
                        echo "Logging in to Amazon ECR"
                        echo "======================================"

                        aws ecr get-login-password \
                            --region "$AWS_REGION" | \
                            docker login \
                            --username AWS \
                            --password-stdin "$ECR_REGISTRY"

                        echo "======================================"
                        echo "Pushing Docker Image"
                        echo "======================================"

                        docker push "$ECR_REPO:$IMAGE_TAG"

                        echo "Docker image pushed successfully."
                    '''
                }
            }
        }

        // ==========================================
        // 6. Test SSH Connection
        // ==========================================
        stage('Test EC2 SSH') {
            steps {

                sshagent(['flask-practice-ec2-ssh']) {

                    sh '''
                        set -e

                        echo "======================================"
                        echo "Testing SSH Connection"
                        echo "======================================"

                        ssh \
                            -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "echo SSH connection successful && hostname"

                        echo "SSH connection successful."
                    '''
                }
            }
        }

        // ==========================================
        // 7. Deploy to EC2
        // ==========================================
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

                            ssh \
                                -o StrictHostKeyChecking=no \
                                ec2-user@98.89.45.250 \
                                "AWS_REGION='$AWS_REGION' \
                                 ECR_REGISTRY='$ECR_REGISTRY' \
                                 ECR_REPO='$ECR_REPO' \
                                 IMAGE_TAG='$IMAGE_TAG' \
                                 MONGO_URI='$MONGO_URI' \
                                 SECRET_KEY='$SECRET_KEY' \
                                 bash -s" <<'REMOTE_SCRIPT'

set -e

echo "======================================"
echo "Connected to EC2"
echo "======================================"

echo "Logging in to Amazon ECR..."

aws ecr get-login-password \
    --region "$AWS_REGION" | \
    docker login \
    --username AWS \
    --password-stdin "$ECR_REGISTRY"

echo "ECR login successful."

echo "======================================"
echo "Pulling New Docker Image"
echo "======================================"

docker pull "$ECR_REPO:$IMAGE_TAG"

echo "Docker image pulled successfully."

echo "======================================"
echo "Stopping Existing Container"
echo "======================================"

docker stop flask-practice || true

echo "Removing Existing Container..."

docker rm flask-practice || true

echo "======================================"
echo "Starting New Container"
echo "======================================"

docker run -d \
    --name flask-practice \
    -p 5000:5000 \
    -e "MONGO_URI=$MONGO_URI" \
    -e "SECRET_KEY=$SECRET_KEY" \
    "$ECR_REPO:$IMAGE_TAG"

echo "======================================"
echo "Container Started"
echo "======================================"

docker ps

echo "======================================"
echo "Deployment Completed Successfully"
echo "======================================"

REMOTE_SCRIPT

                            echo "======================================"
                            echo "EC2 Deployment Finished"
                            echo "======================================"
                        '''
                    }
                }
            }
        }

        // ==========================================
        // 8. Verify Application
        // ==========================================
        stage('Verify Application') {
            steps {

                sshagent(['flask-practice-ec2-ssh']) {

                    sh '''
                        set -e

                        echo "======================================"
                        echo "Verifying Docker Container"
                        echo "======================================"

                        ssh \
                            -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "docker ps --filter name=flask-practice"

                        echo "======================================"
                        echo "Checking Application"
                        echo "======================================"

                        ssh \
                            -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "curl -f http://localhost:5000"

                        echo ""
                        echo "======================================"
                        echo "Application Verification Successful"
                        echo "======================================"
                    '''
                }
            }
        }
    }

    // ==========================================
    // Pipeline Result
    // ==========================================
    post {

        success {
            echo '''
==========================================
CI/CD PIPELINE COMPLETED SUCCESSFULLY!
==========================================
Application built, pushed to ECR,
deployed to EC2 and verified.
'''
        }

        failure {
            echo '''
==========================================
CI/CD PIPELINE FAILED!
==========================================
Check the failed stage in the console log.
'''
        }
    }
}