pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPO = '428409803345.dkr.ecr.ap-south-1.amazonaws.com/ml-date-classifier'
        IMAGE_TAG = "latest"
        EC2_HOST = 'ubuntu@13.127.182.23'
        PEM_KEY = '/var/lib/jenkins/jenkins-key.pem' // Path to your EC2 key
        APP_PORT = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Checking out source code from Git...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t ml-date-classifier:latest .'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                echo '🔐 Logging in to AWS ECR...'
                sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO'
            }
        }

        stage('Push to ECR') {
            steps {
                echo '📤 Tagging and pushing image to ECR...'
                sh '''
                    docker tag ml-date-classifier:latest $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo '🚀 Deploying application on EC2...'
                sh '''
                    ssh -o StrictHostKeyChecking=no -i $PEM_KEY $EC2_HOST "
                        set -e
                        echo '🛑 Stopping old container...'
                        docker rm -f ml-date-classifier || true
                        echo '🧹 Cleaning up old image...'
                        docker rmi $ECR_REPO:$IMAGE_TAG || true
                        echo '📥 Pulling new image from ECR...'
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
                        docker pull $ECR_REPO:$IMAGE_TAG
                        echo '🏃‍♂️ Running new container...'
                        docker run -d -p $APP_PORT:$APP_PORT --name ml-date-classifier $ECR_REPO:$IMAGE_TAG
                    "
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '🩺 Verifying if application is live...'
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://13.127.182.23:5000", returnStdout: true).trim()
                    if (response != '200') {
                        error("❌ Health check failed! App returned HTTP ${response}")
                    } else {
                        echo "✅ Health check passed — App is running successfully."
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Deployment successful and verified!'
        }
        failure {
            echo '💥 Deployment failed. Please check the logs for errors.'
        }
    }
}
