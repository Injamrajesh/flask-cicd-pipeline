pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '310297108115.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = '310297108115.dkr.ecr.us-east-1.amazonaws.com/flask-practice'
        IMAGE_TAG = "${env.GIT_COMMIT}"
        FAILED_STAGE = 'Unknown'
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    env.FAILED_STAGE = 'Checkout'
                }

                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    env.FAILED_STAGE = 'Install Dependencies'
                }

                sh '''
                    set -e

                    echo "======================================"
                    echo "Installing Python Dependencies"
                    echo "======================================"

                    python3 -m pip install \
                        --break-system-packages \
                        -r requirements.txt

                    echo "Dependencies installed successfully."
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    env.FAILED_STAGE = 'Test'
                }

                withCredentials([
                    string(
                        credentialsId: 'MONGO_URI_RI',
                        variable: 'MONGO_URI'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "======================================"
                        echo "Checking MongoDB Credential"
                        echo "======================================"

                        if [ -z "$MONGO_URI" ]; then
                            echo "ERROR: MONGO_URI credential is empty."
                            exit 1
                        fi

                        echo "MongoDB credential is available."

                        echo "======================================"
                        echo "Running Pytest"
                        echo "======================================"

                        python3 -m pytest -v

                        echo "======================================"
                        echo "All tests passed successfully."
                        echo "======================================"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.FAILED_STAGE = 'Build'
                }

                sh '''
                    set -e

                    echo "======================================"
                    echo "Building Docker Image"
                    echo "======================================"

                    echo "Image Tag: $IMAGE_TAG"

                    docker build \
                        -t "$ECR_REPO:$IMAGE_TAG" \
                        .

                    echo "Docker image built successfully."

                    echo "======================================"
                    echo "Docker Image Details"
                    echo "======================================"

                    docker images | grep flask-practice
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                script {
                    env.FAILED_STAGE = 'Push'
                }

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

                        echo "ECR login successful."

                        echo "======================================"
                        echo "Pushing Docker Image"
                        echo "======================================"

                        docker push "$ECR_REPO:$IMAGE_TAG"

                        echo "======================================"
                        echo "Docker Image Pushed Successfully"
                        echo "======================================"

                        echo "Image: $ECR_REPO:$IMAGE_TAG"
                    '''
                }
            }
        }

        stage('Test EC2 SSH') {
            steps {
                script {
                    env.FAILED_STAGE = 'EC2 SSH'
                }

                sshagent(['flask-practice-ec2-ssh']) {
                    sh '''
                        set -e

                        echo "======================================"
                        echo "Testing SSH Connection to EC2"
                        echo "======================================"

                        ssh \
                            -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "echo SSH connection successful && hostname"

                        echo "SSH connection test completed successfully."
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    env.FAILED_STAGE = 'Deploy'
                }

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

echo "======================================"
echo "Logging in to Amazon ECR"
echo "======================================"

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

echo "======================================"
echo "Removing Existing Container"
echo "======================================"

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
echo "Deployment Completed"
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

        stage('Verify Application') {
            steps {
                script {
                    env.FAILED_STAGE = 'Deploy Verification'
                }

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
                        echo "Checking Flask Health Endpoint"
                        echo "======================================"

                        ssh \
                            -o StrictHostKeyChecking=no \
                            ec2-user@98.89.45.250 \
                            "curl -f http://localhost:5000/health"

                        echo ""

                        echo "======================================"
                        echo "Application Verification Successful"
                        echo "======================================"
                    '''
                }
            }
        }
    }

    post {

        success {

            echo '''
==========================================
CI/CD PIPELINE COMPLETED SUCCESSFULLY!
==========================================
Application built, pushed to ECR,
deployed to EC2 and verified using /health.
==========================================
'''

            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

The Jenkins CI/CD pipeline completed successfully.

==============================
BUILD DETAILS
==============================
Job Name     : ${env.JOB_NAME}
Build Number : ${env.BUILD_NUMBER}
Build Status : ${currentBuild.currentResult}
Branch       : ${env.GIT_BRANCH}
Commit SHA   : ${env.GIT_COMMIT}

==============================
DOCKER / ECR
==============================
ECR Repository:
${env.ECR_REPO}

Docker Image Tag:
${env.IMAGE_TAG}

Docker Image:
${env.ECR_REPO}:${env.IMAGE_TAG}

==============================
EC2 DEPLOYMENT
==============================
EC2 Host     : 98.89.45.250
Container    : flask-practice
Port         : 5000
Health Check : PASSED
Endpoint     : /health

==============================
DEPLOYMENT RESULT
==============================
Docker image built successfully.
Docker image pushed to Amazon ECR.
Docker container deployed to EC2.
Application health check passed.

==============================
PIPELINE RUN
==============================
Build URL:
${env.BUILD_URL}

The deployment was successfully completed and verified.

Regards,
Jenkins
""",
                to: "injamrajesh85@gmail.com"
            )
        }

        failure {

            echo '''
==========================================
CI/CD PIPELINE FAILED!
==========================================
Check the failed stage and console log.
==========================================
'''

            emailext(
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello,

The Jenkins CI/CD pipeline has FAILED.

==============================
BUILD DETAILS
==============================
Job Name     : ${env.JOB_NAME}
Build Number : ${env.BUILD_NUMBER}
Build Status : ${currentBuild.currentResult}
Branch       : ${env.GIT_BRANCH}
Commit SHA   : ${env.GIT_COMMIT}

==============================
FAILURE INFORMATION
==============================
Failed Stage:
${env.FAILED_STAGE}

The pipeline stopped after this stage failed.
Subsequent stages were not executed.

==============================
DOCKER / ECR
==============================
ECR Repository:
${env.ECR_REPO}

Docker Image Tag:
${env.IMAGE_TAG}

==============================
PIPELINE LOG
==============================
Build URL:
${env.BUILD_URL}

Console Log:
${env.BUILD_URL}console

Please investigate the failed stage using the Jenkins
console output.

Regards,
Jenkins
""",
                to: "injamrajesh85@gmail.com"
            )
        }
    }
}