ssh -i "~/jenkins-key.pem" ubuntu@13.127.182.23


ubuntu@ip-172-31-7-88:~$ sudo systemctl restart jenkins
ubuntu@ip-172-31-7-88:~$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword
7af303646bb8407181a516402cb97408
ubuntu@ip-172-31-7-88:~$