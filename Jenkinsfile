@Library('my-shared-library') _

pipeline {
    agent any

        environment {
        APP_NAME = "appbyjenkins"
        BRANCH_NAME="BestBranch"
    }
    stages {
        stage('Parallel Build & SonarQube') {
            parallel {
                stage('Build') {
                    steps {
                        script {
                            myLibrary.buildApp()
                        }
                    }
                }
                stage('SonarQube') {
                    steps {
                        script {
                            codeQuality.sonarEcho()
                        }
                    }
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

        stage('Parallel Tests') {
            parallel {
                stage('Test on Chrome') {
            steps {
                script {
                    myLibrary.chromeTest()
                }
            }
        }
        stage('Test on Firefox') {
            steps {
                script {
                    myLibrary.firefoxTest()
                        }
                    }
                }
            }
        }

        stage('Wait for User Approval') {
            steps {
                script {
                    myLibrary.userApproval()
                }
            }
        }

        stage('Continue the pipeline') {
            steps {
                script {
                    myLibrary.continuePipeline()
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