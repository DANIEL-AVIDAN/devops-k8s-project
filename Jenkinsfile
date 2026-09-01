pipeline {
    agent any

        environment {
        APP_NAME = "appbyjenkins"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh "docker build -t danielavidan/${env.APP_NAME}:${env.BUILD_NUMBER} ."
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'danielavidan-dockerhub', usernameVariable: 'Username', passwordVariable: 'Password')]) {
                    echo "Deploying with username $Username"
                    // Use the credentials in your deployment steps
                    sh "docker login -u $Username"
                    sh "docker push danielavidan/${env.APP_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                // Test steps here
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Deploy steps here
            }
        }
    }
}
