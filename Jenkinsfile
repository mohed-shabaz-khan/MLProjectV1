pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '428409803345'           // AWS Account ID
        AWS_REGION = 'ap-south-1'                 // AWS region
        ECR_REPO_NAME = 'ml-date-classifier'      // ECR repository name
        IMAGE_TAG = "latest"                      // Docker image tag
        EC2_USER = 'ec2-user'                     // EC2 default user
        EC2_IP = '13.127.182.23'                  // EC2 instance IP
    }

    stages {
        // STEP 1️⃣: Checkout source code from your GitHub repo
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/mohed-shabaz-khan/MLProjectV1.git'
            }
        }

        // STEP 2️⃣: Build Docker image
        stage('Build Docker Image') {
            steps {
                echo "📦 Building Docker image..."
                sh 'docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .'
            }
        }

        // STEP 3️⃣: Authenticate to AWS ECR securely
        stage('Login to AWS ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    echo "🔐 Configuring AWS credentials..."
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set default.region ${AWS_REGION}

                    echo "🔑 Logging in to AWS ECR..."
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    '''
                }
            }
        }

        // STEP 4️⃣: Tag and push image to ECR
        stage('Tag & Push Image to ECR') {
            steps {
                echo "🚀 Tagging and pushing Docker image to ECR..."
                sh '''
                docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} \
                ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}
                
                docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}
                '''
            }
        }

        // STEP 5️⃣: Deploy container on EC2
        stage('Deploy on EC2') {
            steps {
                echo "🚀 Deploying Docker container to EC2..."
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} '
                    echo "Pulling the latest image from ECR..." &&
                    docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG} &&
                    echo "Stopping old container if running..." &&
                    docker stop ml_app || true &&
                    docker rm ml_app || true &&
                    echo "Starting new container..." &&
                    docker run -d -p 5000:5000 --name ml_app \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}
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
