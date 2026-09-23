pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "animeverse"
        PYTHON_VENV = ".jenkins-venv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out AnimeVerse source code...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                sh '''
                    python3 -m venv ${PYTHON_VENV}
                    ${PYTHON_VENV}/bin/pip install --upgrade pip
                    ${PYTHON_VENV}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests...'

                sh '''
                    ${PYTHON_VENV}/bin/pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building AnimeVerse Docker image...'

                sh '''
                    docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                echo 'Scanning Docker image for HIGH and CRITICAL vulnerabilities...'

                sh '''
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {

        success {
            echo 'AnimeVerse CI/CD security pipeline completed successfully!'
        }

        failure {
            echo 'AnimeVerse pipeline failed. Check the failed stage and console output.'
        }

        always {
            echo 'AnimeVerse pipeline execution completed.'
        }
    }
}
