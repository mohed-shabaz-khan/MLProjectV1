pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '428409803345'           // AWS Account ID
        AWS_REGION = 'ap-south-1'                 // AWS region
        ECR_REPO_NAME = 'ml-date-classifier'      // ECR repository name
        IMAGE_TAG = "latest"                      // Docker image tag
        EC2_USER = 'ubuntu'                       // EC2 username (use 'ec2-user' if Amazon Linux)
        EC2_IP = '13.127.182.23'                  // EC2 instance Public IP
    }

    stages {

        // STEP 1️⃣: Checkout source code
        stage('Checkout Code') {
            steps {
                echo "🔄 Checking out code from GitHub..."
                git branch: 'main', url: 'https://github.com/mohed-shabaz-khan/MLProjectV1.git'
            }
        }

        // STEP 2️⃣: Build Docker image
        stage('Build Docker Image') {
            steps {
                echo "📦 Building Docker image..."
                sh '''
                set -e
                docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        // STEP 3️⃣: Login to AWS ECR securely
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

        // STEP 4️⃣: Tag & Push image to ECR
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

        // STEP 5️⃣: Deploy on EC2
        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying Docker container on EC2..."
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    set -e
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} '
                    set -e
                    echo "📥 Pulling latest Docker image from ECR..."
                    sudo docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

                    echo "🧹 Cleaning up old container (if any)..."
                    sudo docker stop ml_app || true
                    sudo docker rm ml_app || true

                    echo "🚀 Starting new container..."
                    sudo docker run -d -p 5000:5000 --name ml_app \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

                    echo "✅ Deployment successful on EC2!"
                    '
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ SUCCESS: MLProjectV1 deployed successfully to EC2!'
        }
        failure {
            echo '❌ FAILURE: Something went wrong during deployment. Check Jenkins logs.'
        }
    }
}
