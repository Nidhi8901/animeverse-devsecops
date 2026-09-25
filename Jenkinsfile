pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "animeverse"
        AWS_REGION = "ap-south-1"
        ECR_REGISTRY = "577638393088.dkr.ecr.ap-south-1.amazonaws.com"
        ECR_REPOSITORY = "animeverse"
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

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube code quality analysis...'

                withSonarQubeEnv('SonarQube') {
                    withCredentials([
                        string(
                            credentialsId: 'sonarqube-token',
                            variable: 'SONAR_TOKEN'
                        )
                    ]) {
                        sh '''
                            ${PYTHON_VENV}/bin/pip install --quiet pysonar

                            SONAR_HOST_URL="${SONAR_HOST_URL}" \
                            SONAR_TOKEN="${SONAR_TOKEN}" \
                            ${PYTHON_VENV}/bin/pysonar
                        '''
                    }
                }
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
                echo 'Running Trivy vulnerability scan...'

                sh '''
                    trivy image \
                    --scanners vuln \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    --exit-code 0 \
                    ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                echo 'Authenticating with AWS and pushing AnimeVerse image to ECR...'

                withCredentials([
                    aws(
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        credentialsId: 'aws-credentials',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        aws sts get-caller-identity

                        aws ecr get-login-password \
                            --region ${AWS_REGION} | \
                            docker login \
                            --username AWS \
                            --password-stdin ${ECR_REGISTRY}

                        docker tag \
                            ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                        docker tag \
                            ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest

                        docker push \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                        docker push \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                    '''
                }
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

