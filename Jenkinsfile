pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "mostakimidlc/asseto-asset-management"
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        GITHUB_CREDENTIALS_ID = 'github-creds'
        PROD_DIR = '/opt/asseto-production'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code from GitHub..."
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                script {
                    docker.withRegistry('', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo "Deploying to production environment..."
                script {
                    sh """
                        # Verify production directory exists
                        echo "Checking production directory..."
                        ls -la ${PROD_DIR}
                        
                        # Copy docker-compose configuration
                        echo "Copying docker-compose file..."
                        cp docker-compose.prod.yml ${PROD_DIR}/docker-compose.yml
                        
                        # Copy environment file if it exists
                        if [ -f .env.production ]; then
                            echo "Copying environment file..."
                            cp .env.production ${PROD_DIR}/.env
                        else
                            echo "Warning: .env.production not found, using existing or default env"
                        fi
                        
                        # Navigate to production directory and deploy
                        cd ${PROD_DIR}
                        
                        echo "Stopping existing containers..."
                        docker-compose down || true
                        
                        echo "Pulling latest images..."
                        docker-compose pull
                        
                        echo "Starting containers..."
                        docker-compose up -d
                        
                        # Wait for services to start
                        echo "Waiting for services to start..."
                        sleep 10
                        
                        echo "Checking container status..."
                        docker-compose ps
                        
                        echo "Recent logs:"
                        docker-compose logs --tail=30
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo "Performing health check..."
                script {
                    sh """
                        cd ${PROD_DIR}
                        
                        # Check if containers are running
                        RUNNING=\$(docker-compose ps --services --filter "status=running" | wc -l)
                        echo "Running containers: \$RUNNING"
                        
                        if [ \$RUNNING -eq 0 ]; then
                            echo "ERROR: No containers are running!"
                            docker-compose logs --tail=50
                            exit 1
                        fi
                        
                        # Optional: Check if web service responds
                        # sleep 5
                        # curl -f http://localhost:8000 || exit 1
                        
                        echo "Deployment successful!"
                    """
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "Cleaning up old Docker images..."
                script {
                    sh """
                        # Remove dangling images
                        docker image prune -f
                        
                        # Remove old images (keep last 3 builds)
                        docker images ${DOCKER_IMAGE} --format "{{.Tag}}" | \
                        grep -v latest | \
                        sort -rn | \
                        tail -n +4 | \
                        xargs -I {} docker rmi ${DOCKER_IMAGE}:{} || true
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
            echo "Application deployed to production at ${PROD_DIR}"
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
            script {
                sh """
                    cd ${PROD_DIR}
                    echo "Container status:"
                    docker-compose ps
                    echo "Recent logs:"
                    docker-compose logs --tail=100
                """
            }
        }
    }
}
