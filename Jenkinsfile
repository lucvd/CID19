pipeline {
    agent any

    stages {
        stage('Test main') {
            steps {
                withCredentials([file(credentialsId: 'secrets_CID19', variable: 'secretsdjango')]) {
                    script {
                        if(isUnix()){
                            sh label: '', script: 'runtest.sh'
                        }else{
                            bat label: '', script: 'runtest.bat'
                        }
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                bat label: '', script: 'runDeploy.bat'
            }
        }
        stage('Test Browserstack') {
            steps {
                withCredentials([file(credentialsId: 'browserstack_config', variable: 'CONFIG_FILE')]) {
                    browserstack('8634eb5c-bcf0-418d-a0e2-ecb84b185250') {
                        script {
                            if(isUnix()){
                                sh label: '', script: 'runBrowserstack.sh'
                            }else{
                                bat label: '', script: 'runBrowserstack.bat'
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            junit '**/reports/*.xml'
            recordIssues(tools: [pyLint(pattern: 'reports/pylint.report'), pep8(pattern: 'reports/pep8.report')])
            cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
        }
        failure {
            emailext body: 'An error needs to be fixed asap!', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'An error occured in the ConnectID pipeline'
        }
    }
}
