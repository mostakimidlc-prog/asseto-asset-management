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

        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production environment...'
                sh '''
                    PROD_DIR="/opt/asseto-production"
                    
                    # Ensure production directory exists
                    sudo mkdir -p ${PROD_DIR}/{secrets,backups,logs}
                    sudo chown -R jenkins:jenkins ${PROD_DIR}
                    sudo chmod 700 ${PROD_DIR}/secrets
                    
                    # Copy production docker-compose to production directory
                    cp ${WORKSPACE}/docker-compose.prod.yml ${PROD_DIR}/docker-compose.yml
                    
                    # Verify secrets exist (fail if missing)
                    if [ ! -f "${PROD_DIR}/secrets/django.env" ]; then
                        echo "✗ Error: django.env not found!"
                        echo "Please create secrets files first. See documentation."
                        exit 1
                    fi
                    
                    if [ ! -f "${PROD_DIR}/secrets/database.env" ]; then
                        echo "✗ Error: database.env not found!"
                        exit 1
                    fi
                    
                    if [ ! -f "${PROD_DIR}/secrets/admin.env" ]; then
                        echo "✗ Error: admin.env not found!"
                        exit 1
                    fi
                    
                    echo "✓ All required secrets files found"
                    
                    # Navigate to production directory
                    cd ${PROD_DIR}
                    
                    # Pull latest image
                    echo "Pulling latest Docker image..."
                    docker pull ${DOCKER_IMAGE}:latest
                    
                    # Backup database before deployment
                    echo "Creating database backup..."
                    BACKUP_FILE="backups/backup_$(date +%Y%m%d_%H%M%S).sql"
                    docker exec asseto-postgres-prod pg_dump -U asseto_user asseto_db > ${BACKUP_FILE} 2>/dev/null || echo "Note: Backup skipped (first deployment or database not ready)"
                    
                    # Stop only web container
                    echo "Stopping web container..."
                    docker stop asseto-web-prod 2>/dev/null || true
                    docker rm asseto-web-prod 2>/dev/null || true
                    
                    # Start services
                    echo "Starting services..."
                    docker-compose up -d
                    
                    # Wait for application
                    echo "Waiting for application to start..."
                    sleep 30
                    
                    # Health check
                    echo "Performing health check..."
                    for i in {1..10}; do
                        if curl -sf http://localhost:8002/admin/login/ > /dev/null 2>&1; then
                            echo "✓ Application is healthy!"
                            docker ps --filter "name=asseto-.*-prod" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
                            echo ""
                            echo "Deployment successful!"
                            echo "Application: http://localhost:8002"
                            echo "Admin Panel: http://localhost:8002/admin/"
                            exit 0
                        fi
                        echo "Attempt $i/10..."
                        sleep 5
                    done
                    
                    echo "✗ Health check failed!"
                    docker logs asseto-web-prod --tail=100
                    exit 1
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
