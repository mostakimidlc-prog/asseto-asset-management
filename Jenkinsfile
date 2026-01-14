pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "mostakimidlc/asseto-asset-management"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = 'dockerhub-creds'
        CONTAINER_NAME = 'asseto-web'
        DB_CONTAINER_NAME = 'asseto-postgres'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
  
      
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    // Leave URL empty for default Docker Hub
                    docker.withRegistry('', DOCKER_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
	        }
            }
        }


        stage('Deploy Application') {
            steps {
                echo 'Deploying application...'
                sh '''
                    # Navigate to project directory
                    echo "Current workspace: $WORKSPACE"
                    cd $WORKSPACE
                    
                    # Stop existing containers
                    docker-compose down --remove-orphans || true
                    docker rm -f asseto-web asseto-postgres || true
                    
                    # Pull latest image
                    docker pull ${DOCKER_IMAGE}:latest
                    
                    # Start containers with latest image
                    docker-compose up -d
                    
                    # Wait for application to start
                    sleep 10
                    
                    # Check application health
                    curl -f http://localhost:8002/ || exit 1
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up old Docker images...'
                sh '''
                    # Remove dangling images
                    docker image prune -f
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            echo "Application is running at: http://localhost:8002"
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}
