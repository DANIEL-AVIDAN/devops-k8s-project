pipeline {
    agent any

        environment {
        APP_NAME = "MyApp"
    }


    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                docker build -t ${env.APP_NAME}:${env.BUILD_NUMBER} .`
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



