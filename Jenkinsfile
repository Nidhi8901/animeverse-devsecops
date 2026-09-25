pipeline {

agent any

environment {
    DOCKER_IMAGE = "animeverse"
    AWS_REGION = "ap-south-1"

    ECR_REGISTRY = "577638393088.dkr.ecr.ap-south-1.amazonaws.com"
    ECR_REPOSITORY = "animeverse"

    ECS_CLUSTER = "animeverse-cluster"
    ECS_SERVICE = "ideal-server-bbh73yanimeverse-task-service-10phphdy"
    ECS_TASK_DEFINITION = "ideal-server-bbh73yanimeverse-task"
    ECS_CONTAINER_NAME = "animeverse"

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
                docker build \
                    -t ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                    .
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

                    echo "Checking AWS identity..."
                    aws sts get-caller-identity

                    echo "Logging in to Amazon ECR..."

                    aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                        docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}

                    echo "Tagging Docker image..."

                    docker tag \
                        ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                    docker tag \
                        ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest

                    echo "Pushing build-specific image..."

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}

                    echo "Pushing latest image..."

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest

                    echo "AnimeVerse image pushed successfully to ECR."
                '''
            }
        }
    }

    stage('Deploy to ECS') {
        steps {
            echo 'Deploying AnimeVerse to ECS Fargate...'

            withCredentials([
                aws(
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    credentialsId: 'aws-credentials',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                )
            ]) {

                sh '''
                    set -e

                    echo "Downloading current ECS task definition..."

                    aws ecs describe-task-definition \
                        --task-definition ${ECS_TASK_DEFINITION} \
                        --region ${AWS_REGION} \
                        --query 'taskDefinition' \
                        --output json > task-definition.json

                    echo "Creating task definition update script..."

                    printf '%s\\n' \
                    'import json' \
                    'import os' \
                    '' \
                    'with open("task-definition.json", "r") as f:' \
                    '    task = json.load(f)' \
                    '' \
                    'new_image = os.environ["NEW_IMAGE"]' \
                    'container_name = os.environ["ECS_CONTAINER_NAME"]' \
                    '' \
                    'for container in task["containerDefinitions"]:' \
                    '    if container["name"] == container_name:' \
                    '        container["image"] = new_image' \
                    '' \
                    'fields_to_remove = [' \
                    '    "taskDefinitionArn",' \
                    '    "revision",' \
                    '    "status",' \
                    '    "requiresAttributes",' \
                    '    "compatibilities",' \
                    '    "registeredAt",' \
                    '    "registeredBy"' \
                    ']' \
                    '' \
                    'for field in fields_to_remove:' \
                    '    task.pop(field, None)' \
                    '' \
                    'with open("new-task-definition.json", "w") as f:' \
                    '    json.dump(task, f)' \
                    > update_task_definition.py

                    echo "Updating container image in task definition..."

                    NEW_IMAGE="${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}" \
                    ECS_CONTAINER_NAME="${ECS_CONTAINER_NAME}" \
                    python3 update_task_definition.py

                    echo "Registering new ECS task definition..."

                    NEW_TASK_DEFINITION=$(aws ecs register-task-definition \
                        --cli-input-json file://new-task-definition.json \
                        --region ${AWS_REGION} \
                        --query 'taskDefinition.taskDefinitionArn' \
                        --output text)

                    echo "New task definition:"
                    echo "${NEW_TASK_DEFINITION}"

                    echo "Updating ECS service..."

                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --task-definition ${NEW_TASK_DEFINITION} \
                        --region ${AWS_REGION}

                    echo "Waiting for ECS service to become stable..."

                    aws ecs wait services-stable \
                        --cluster ${ECS_CLUSTER} \
                        --services ${ECS_SERVICE} \
                        --region ${AWS_REGION}

                    echo "AnimeVerse deployed successfully to ECS Fargate."

                    rm -f task-definition.json
                    rm -f new-task-definition.json
                    rm -f update_task_definition.py
                '''
            }
        }
    }
}

post {

    success {
        echo 'AnimeVerse CI/CD security and deployment pipeline completed successfully!'
    }

    failure {
        echo 'AnimeVerse pipeline failed. Check the failed stage and console output.'
    }

    always {
        echo 'AnimeVerse pipeline execution completed.'
    }
}

}