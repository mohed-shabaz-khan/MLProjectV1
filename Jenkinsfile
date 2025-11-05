pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '428409803345'           // AWS Account ID
        AWS_REGION = 'ap-south-1'                 // AWS region
        ECR_REPO_NAME = 'ml-date-classifier'      // ECR repository name
        IMAGE_TAG = "latest"                      // Docker image tag
        EC2_USER = 'ubuntu'                       // EC2 username (use 'ec2-user' for Amazon Linux)
        EC2_IP = '13.235.76.77'                     // EC2 public IP
        APP_PORT = '5000'                         // EC2 external port for FastAPI app
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "🔄 Checking out code from GitHub..."
                git branch: 'main', url: 'https://github.com/mohed-shabaz-khan/MLProjectV1.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "📦 Building Docker image..."
                sh '''
                set -e
                docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Login to AWS ECR') {
            steps {
                echo "🔑 Logging in to AWS ECR..."
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    set -e
                    echo "🔐 Configuring AWS credentials..."
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region ${AWS_REGION}

                    echo "🔑 Logging into ECR..."
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag & Push Image to ECR') {
            steps {
                echo "🚀 Tagging and pushing Docker image to ECR..."
                sh '''
                set -e
                docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} \
                ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

                docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying Docker container on EC2..."
                sshagent(['ec2-ssh-key']) {
                    sh """
                    set -e
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "
                    set -e
                    echo '🔐 Logging in to AWS ECR on EC2...'
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    sudo docker login --username AWS --password-stdin \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    echo '📥 Pulling latest Docker image from ECR...'
                    sudo docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

                    echo '🧹 Cleaning up old container (if any)...'
                    sudo docker stop ml_app || true
                    sudo docker rm ml_app || true

                    echo '🚀 Starting new container on port ${APP_PORT}...'
                    sudo docker run -d -p ${APP_PORT}:8080 --name ml_app \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

                    echo '✅ Deployment successful on EC2!'
                    "
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                echo '🩺 Checking FastAPI service health...'
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://${EC2_IP}:${APP_PORT}/health", returnStdout: true).trim()
                    if (response != '200') {
                        error("❌ Health check failed! App returned HTTP ${response}")
                    } else {
                        echo "✅ Health check passed — FastAPI app is running on port ${APP_PORT}."
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 SUCCESS: MLProjectV1 deployed and verified successfully to EC2!'
        }
        failure {
            echo '💥 FAILURE: Something went wrong during deployment. Check Jenkins logs.'
        }
    }
}

