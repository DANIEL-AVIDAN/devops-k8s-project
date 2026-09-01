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
                withCredentials([usernamePassword(
                    credentialsId: 'danielavidan-dockerhub',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        printf '%s' "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push danielavidan/${APP_NAME}:${BUILD_NUMBER}
                    '''
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
