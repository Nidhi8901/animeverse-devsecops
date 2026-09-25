AnimeVerse — AWS DevSecOps CI/CD Pipeline

AnimeVerse is an anime wallpaper web application deployed through an automated DevSecOps CI/CD pipeline using Jenkins, Docker, SonarQube, Trivy, Amazon ECR, Amazon ECS Fargate, and an Application Load Balancer.

The project demonstrates how application code can move from GitHub to a production-style AWS container deployment while automated testing, code-quality analysis, and container security scanning are performed during the pipeline.

Architecture
                    ┌─────────────────────┐
                    │       GitHub        │
                    │  AnimeVerse Source  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Jenkins       │
                    │    CI/CD Pipeline   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐   ┌────────────┐   ┌────────────┐
        │   Pytest  │   │ SonarQube  │   │   Trivy    │
        │   Tests   │   │ Code Scan  │   │Image Scan  │
        └───────────┘   └────────────┘   └────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Docker Image      │
                    │     Build           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Amazon ECR       │
                    │ Container Registry  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Amazon ECS        │
                    │     Fargate         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Application Load    │
                    │     Balancer        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     AnimeVerse      │
                    │   Web Application   │
                    └─────────────────────┘
Project Overview

The goal of this project is to implement a complete DevSecOps workflow for a Python Flask web application.

The pipeline automatically:

Retrieves source code from GitHub.
Creates a Python virtual environment.
Installs application dependencies.
Runs automated tests using Pytest.
Performs static code-quality analysis using SonarQube.
Builds the application into a Docker image.
Scans the Docker image using Trivy.
Pushes the container image to Amazon ECR.
Registers a new ECS task-definition revision.
Updates the ECS Fargate service.
Waits for the ECS service to become stable.

This creates an automated path from source code to a running containerized application.

Technologies Used
Application
Python
Flask
Gunicorn
HTML/CSS
Pytest
DevOps
Git
GitHub
Jenkins
Docker
DevSecOps
SonarQube
Trivy
AWS
Amazon ECR
Amazon ECS
AWS Fargate
Application Load Balancer
IAM
Amazon CloudWatch
Amazon VPC
Security Groups
Application Features

AnimeVerse provides an anime wallpaper web interface with categories including:

Demon Slayer
Jujutsu Kaisen
Tokyo Revengers
Wind Breaker

The application provides:

Anime wallpaper browsing
Category-based wallpaper display
Wallpaper download functionality
REST API endpoint
Application health endpoint
Health Endpoint
/health

Example response:

{
  "status": "healthy",
  "application": "AnimeVerse"
}
Wallpaper API
/api/wallpapers
Repository Structure
animeverse-devsecops/
│
├── app/
│   ├── app.py
│   └── templates/
│       └── index.html
│
├── tests/
│   └── ...
│
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
CI/CD Pipeline

The Jenkins pipeline is implemented as Pipeline as Code using a Jenkinsfile stored in the GitHub repository.

The pipeline contains the following stages:

1. Checkout

Jenkins retrieves the latest application source code from GitHub.

2. Setup Python Environment

A Python virtual environment is created inside the Jenkins workspace.

Dependencies are installed from:

requirements.txt
3. Run Tests

Automated tests are executed using:

pytest -v

The application tests validate the main application functionality.

4. SonarQube Analysis

The source code is analyzed using SonarQube to identify code-quality issues and maintainability problems.

5. Build Docker Image

Jenkins builds the AnimeVerse container image:

docker build -t animeverse:${BUILD_NUMBER} .
6. Trivy Security Scan

The Docker image is scanned using Trivy.

The pipeline checks for:

HIGH vulnerabilities
CRITICAL vulnerabilities

Unfixed vulnerabilities are ignored during the pipeline scan.

7. Push Image to Amazon ECR

Jenkins authenticates with Amazon ECR and pushes:

BUILD_NUMBER

and:

latest

image tags.

8. Deploy to ECS Fargate

Jenkins:

Retrieves the current ECS task definition.
Updates the container image.
Registers a new task-definition revision.
Updates the ECS service.
Waits for the ECS service to become stable.

Docker

The application is containerized using a Python slim base image.

The container exposes:

8000

The application is started using Gunicorn:

gunicorn --bind 0.0.0.0:8000 app.app:app

Amazon ECR

The Docker image is stored in an Amazon ECR repository.

Repository:

animeverse

AWS Region:

ap-south-1

Example image:

577638393088.dkr.ecr.ap-south-1.amazonaws.com/animeverse:latest

Build-specific image tags are also pushed by Jenkins.

Amazon ECS Fargate

The application is deployed as a containerized workload on Amazon ECS using AWS Fargate.

The ECS architecture consists of:

ECS Cluster
      │
      ▼
ECS Service
      │
      ▼
Fargate Task
      │
      ▼
AnimeVerse Container

Fargate removes the need to manage EC2 servers for the application container.

Application Load Balancer

An Application Load Balancer provides external access to the AnimeVerse application.

Traffic flow:

Internet
   │
   ▼
Application Load Balancer
   │
   ▼
Target Group
   │
   ▼
ECS Fargate Task :8000

The target group performs health checks against the application.

Security

Security is incorporated directly into the CI/CD pipeline.

SonarQube

Used for source-code quality analysis.

Trivy

Used to scan the Docker image for known vulnerabilities before deployment.

IAM

AWS IAM controls access to AWS resources used by the deployment pipeline.

Security Groups

Network access is restricted between the Application Load Balancer and ECS task.

The ECS application listens on:

TCP 8000

while the Application Load Balancer receives HTTP traffic.

Jenkins AWS Authentication

Jenkins uses an AWS credential configured in Jenkins Credentials Manager.

The pipeline uses the credentials only inside the AWS deployment stages.

AWS credentials are not stored in the GitHub repository.

Local Setup
Clone the repository
git clone https://github.com/Nidhi8901/animeverse-devsecops.git
cd animeverse-devsecops
Create a virtual environment
python -m venv venv
Activate it on Git Bash
source venv/Scripts/activate
Install dependencies
pip install -r requirements.txt
Run tests
pytest -v
Run the application
python app/app.py

The application runs on:

http://localhost:8000
Docker Setup

Build the image:

docker build -t animeverse .

Run the container:

docker run -p 8000:8000 animeverse

Open:

http://localhost:8000
DevSecOps Workflow

The complete workflow is:

Developer
    │
    ▼
GitHub
    │
    ▼
Jenkins
    │
    ├── Checkout
    │
    ├── Python Environment
    │
    ├── Pytest
    │
    ├── SonarQube
    │
    ├── Docker Build
    │
    ├── Trivy Scan
    │
    ├── ECR Push
    │
    └── ECS Deployment
             │
             ▼
       AWS Fargate
             │
             ▼
           ALB
             │
             ▼
        AnimeVerse
Key DevSecOps Practices Demonstrated
Pipeline as Code
Automated testing
Continuous Integration
Static code analysis
Containerization
Container vulnerability scanning
Container registry management
Automated cloud deployment
AWS IAM-based authentication
ECS Fargate deployment
Load balancing
Application health checks
Automated deployment validation
Project Outcome

The project demonstrates an end-to-end DevSecOps pipeline in which a code change can progress from GitHub through automated testing and security checks before being packaged into a Docker image, stored in Amazon ECR, and deployed to an ECS Fargate service behind an Application Load Balancer.

The infrastructure was used as a project environment and can be removed after testing to avoid unnecessary ongoing AWS resource usage.

Screenshots

Recommended project evidence:

GitHub

Add:

screenshots/github-repository.png
Jenkins Pipeline

Add:

screenshots/jenkins-success.png
SonarQube

Add:

screenshots/sonarqube-analysis.png
Trivy

Add:

screenshots/trivy-scan.png
Amazon ECR

Add:

screenshots/ecr-image.png
Amazon ECS

Add:

screenshots/ecs-service.png
Application Load Balancer

Add:

screenshots/alb-target-health.png
AnimeVerse

Add:

screenshots/animeverse-homepage.png
Author

Nidhi Kumari

DevOps / Cloud DevOps

GitHub:

https://github.com/Nidhi8901
