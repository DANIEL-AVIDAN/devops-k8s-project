@Library('my-shared-library') _

pipeline {
    agent any

        environment {
        APP_NAME = "appbyjenkins"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    myLibrary.buildApp()
                }
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'danielavidan-dockerhub',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                   echo 'Pushing...'
                    script {
                        myLibrary.pushApp()
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    myLibrary.testApp()
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    myLibrary.deployApp(env.BRANCH_NAME)
                }
            }
        }
    }
}