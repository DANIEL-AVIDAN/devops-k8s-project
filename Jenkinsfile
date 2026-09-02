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
                    // Wait for user interaction and store the result
                    def userInput = input message: 'Is the application running successfully?',
                                         parameters: [choice(name: 'Continue', choices: 'Continue\nCancel', description: 'Choose an option')]
                    // Set a variable based on user input
                    env.USER_CHOICE = userInput
                }
            }
        }

                stage('Continue the pipeline') {
                    // Run this stage ONLY! if the user chooses 'Proceed'

                    when {
                        expression { env.USER_CHOICE == 'Continue' }
                    }
                    steps {
                        script {
                            echo 'Continuing the pipeline...'
                        }
                    }
                }

                stage('Abort the Pipeline') {
                    // Run this stage ONLY! if the user chooses 'Abort'
                    when {
                        expression { env.USER_CHOICE == 'nCancel' }
                    }
                    steps {
                        script {
                            error 'Pipeline aborted by the user'
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