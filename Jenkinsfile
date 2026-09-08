def appname = "myapp"  // Replace with your application name
def repo = "myproject"  // Replace with your DockerHub username
def appimage = "${repo}/${appname}"
def apptag = "${env.BUILD_NUMBER}"

podTemplate(containers: [
      containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent', ttyEnabled: true),
      containerTemplate(name: 'docker', image: 'docker:dind', ttyEnabled: true, privileged: true),
      containerTemplate(name: 'trivy', image: 'aquasec/trivy:latest', command: 'cat',ttyEnabled: true)
  ],
      // <<< שינוי 2: הוספנו volume ל-Docker daemon
    volumes: [
        emptyDirVolume(
            mountPath: '/var/lib/docker',
            memory: false
        )
    ])
  {
    node(POD_LABEL) {
        stage('chackout') {
            container('jnlp') {
            sh '/usr/bin/git config --global http.sslVerify false'
	    checkout scm
          }
        } // end chackout

        stage('Parallel Build & SonarQube') {
            parallel(
                build: {
                    stage('build') {
                        container('docker') {
                            echo "Building docker image..."
                            dockerImage = docker.build("danielavidan/${appname}:${apptag}")
                        }
                    }
                },

                codeScan: {
                    stage('codeScan') {
                        container('trivy') {
                            echo "Scanning the code..."
                            sh '''
                                trivy fs \
                                    --format json \
                                    --output trivy-report.json \
                                    .
                            '''

                            archiveArtifacts(
                                artifacts: 'trivy-report.json',
                                fingerprint: true
                            )
                        }
                    }
                }
            )
        }

     stage('push') {
            container('docker') {
              script {
                docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                  dockerImage.push()
                }
              }
            }
        } //end push

    }
}
