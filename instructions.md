ssh -i "~/jenkins-key.pem" ubuntu@13.127.182.23
ssh -i "~/jenkins-key.pem" ubuntu@3.7.55.120

ubuntu@ip-172-31-7-88:~$ sudo systemctl restart jenkins
ubuntu@ip-172-31-7-88:~$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword
7af303646bb8407181a516402cb97408
ubuntu@ip-172-31-7-88:~$

curl -X POST "http://3.7.55.120:8080/predict" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Manufacture Date: 12/03/2025"]}'
        stage('Health Check') {
            steps {
                echo '🩺 Verifying if application is live...'
                script {
                    // Updated to use port 8080 and /health endpoint
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://3.7.55.120:8080/health", returnStdout: true).trim()
                    if (response != '200') {
                        error("❌ Health check failed! App returned HTTP ${response}")
                    } else {
                        echo "✅ Health check passed — App is running successfully on port 8080."
                    }
                }
            }
        }