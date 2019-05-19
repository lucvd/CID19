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
            }
        }
        stage('Test Browserstack') {
            steps {
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
    post {
        always {
            junit '**/reports/*.xml'
            junit testDataPublishers: [[$class: 'AutomateTestDataPublisher']], testResults: 'Browserstack_tests/reports/0/*.xml'
            junit 'Browserstack_tests/reports/1/*.xml'
            junit '**/Browserstack_tests/reports/2/*.xml'
            junit 'Browserstack_tests/reports/3/*.xml'
            recordIssues(tools: [pep8(pattern: 'reports/pep8.report')])
            // emailext body: 'I just wanted to say... \n Thanks', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'Test'
            cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
        }
        failure {
            emailext body: 'PipelineTest has failed omg!!!', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'EMERGENCY WII U WII U WII U WII U'
        }
    }
}
