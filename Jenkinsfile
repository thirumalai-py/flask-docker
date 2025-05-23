pipeline {
    agent any

    environment {
        GITREPO = "https://github.com/thirumalai-py/flask-docker"
        GIT_BRANCH = "main"
        EC2_SSH = "thiru-ec2"
        EC2_USER = "ubuntu"
        EC2_HOST = "13.201.229.37"
        CONTAINER_NAME = "thiru-flask"
        DOCKER_IMAGE = "thirumalaipy/flask"
        DOCKER_CREDENTIALS_ID = "thiru-docker-cred"
        DOCKER_REGISTRY = "https://index.docker.io/v1"
        DOCKER_NETWORK = "app-network"
        ALERT_EMAIL = "thirumalai.py@gmail.com"
    }

    stages {
        stage('Get Build Number') { 
            steps {
                echo "Build Number: ${BUILD_NUMBER}"
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GITREPO}"
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh '''
                            echo "Removing existing MongoDB container if it exists..."
                            docker rm -f mongo-db || true

                            echo "Starting MongoDB with seed data..."
                            docker-compose up -d mongo-db

                            echo "Waiting for MongoDB to be ready..."
                            max_attempts=30
                            attempt=0
                            while [ $attempt -lt $max_attempts ]; do
                                docker-compose exec -T mongo-db mongosh --eval "db.runCommand({ping:1})" && break
                                echo "Waiting for MongoDB to be ready... (attempt $attempt)"
                                sleep 2
                                attempt=$((attempt+1))
                            done

                            if [ $attempt -eq $max_attempts ]; then
                                echo "MongoDB did not become ready in time"
                                exit 1
                            fi

                            echo "MongoDB is ready. Running tests..."
                            mkdir -p test-reports
                            docker-compose run --rm test pytest --maxfail=1 --disable-warnings --junitxml=test-reports/test-results.xml
                        '''
                    } catch (Exception e) {
                        echo "Test stage failed: ${e.getMessage()}"
                        throw e
                    } finally {
                        sh 'docker-compose down -v || true'
                    }
                }
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                }
                failure {
                    echo "Tests failed. Check the test reports for details."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Test Docker Credentials') {
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        echo "Docker credentials are valid."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['thiru-ec2']) {
                    sh """
                        echo "Deploying to EC2..."

                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            echo "Checking if Docker network ${DOCKER_NETWORK} exists..."
                            docker network inspect ${DOCKER_NETWORK} > /dev/null 2>&1 || docker network create ${DOCKER_NETWORK}

                            echo "Checking if mongo_data volume exists..."
                            docker volume inspect mongo_data > /dev/null 2>&1 || docker volume create mongo_data

                            echo "Checking if MongoDB container exists..."
                            MONGO_CONTAINER=\$(docker ps -a -f name=mongo-db -q)

                            if [ -z "\$MONGO_CONTAINER" ]; then
                                echo "Creating MongoDB container..."
                                docker run -d --name mongo-db --network ${DOCKER_NETWORK} \
                                    -p 27017:27017 \
                                    -v mongo_data:/data/db \
                                    -e MONGO_INITDB_DATABASE=flask_db \
                                    mongo:latest
                            else
                                if [ -z "\$(docker ps -f name=mongo-db -q)" ]; then
                                    echo "Starting existing MongoDB container..."
                                    docker start mongo-db
                                fi
                                echo "Connecting MongoDB container to network if not already connected..."
                                docker network connect ${DOCKER_NETWORK} mongo-db || true
                            fi

                            echo "Pulling Flask Application Image..."
                            docker pull ${DOCKER_IMAGE}:${BUILD_NUMBER}

                            echo "Stopping existing Flask container if running..."
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true

                            echo "Starting new Flask container connected to network ${DOCKER_NETWORK}..."
                            docker run -d --name ${CONTAINER_NAME} --network ${DOCKER_NETWORK} \
                                -p 8000:8000 \
                                -e MONGO_URI=mongodb://mongo-db:27017/flask_db \
                                -e JWT_SECRET_KEY=thirumalaipy \
                                -e MONGO_DB_NAME=flask_db \
                                ${DOCKER_IMAGE}:${BUILD_NUMBER}

                            echo "Deployment done."
                        '
                    """
                }
            }
        }
    }

     post {
        failure {
            echo 'Build or test failed. Sending notifications...'
            emailext(
    subject: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    body: """\
<html>
<body>
<h3>Flask Application Build FAILED ❌</h3>
<p><strong>Job:</strong> ${env.JOB_NAME}</p>
<p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
<p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
<p><strong>Git Repo:</strong> ${env.GITREPO}</p>
<p><strong>Docker Image:</strong> ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}</p>
<p><strong>EC2 Host:</strong> ${env.EC2_HOST}</p>
<p><strong>Failure Time:</strong> ${new Date().format("yyyy-MM-dd HH:mm:ss", TimeZone.getTimeZone("Asia/Kolkata"))}</p>
<p><a href="${env.BUILD_URL}">Click here to view full build logs</a></p>
</body>
</html>
""",
    mimeType: 'text/html',
    to: "${ALERT_EMAIL}"
)

        }
        success {
            echo 'Build and deployment passed successfully!'
            emailext(
    subject: "✅ Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    body: """\
<html>
<body>
<h3>Flask Application Build & Deployment SUCCEEDED ✅</h3>
<p><strong>Job:</strong> ${env.JOB_NAME}</p>
<p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
<p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
<p><strong>Git Repo:</strong> ${env.GITREPO}</p>
<p><strong>Docker Image:</strong> ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}</p>
<p><strong>Deployed To:</strong> EC2 (${env.EC2_HOST})</p>
<p><strong>Deployment Time:</strong> ${new Date().format("yyyy-MM-dd HH:mm:ss", TimeZone.getTimeZone("Asia/Kolkata"))}</p>
<p><a href="${env.BUILD_URL}">Click here to view full build logs</a></p>
</body>
</html>
""",
    mimeType: 'text/html',
    to: "${ALERT_EMAIL}"
)

            script {
                sh '''
                    echo "===== Deployment Success Summary ====="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Docker Image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    echo "Deployment Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
                    
                    echo "\n----- Docker Images -----"
                    docker images | grep "${DOCKER_IMAGE}"
                    
                    echo "\n----- Running Containers -----"
                    docker ps
                    
                    echo "\n----- Disk Space -----"
                    df -h
                    
                    echo "\n----- Docker System Info -----"
                    docker system info
                    
                    echo "\n----- Cleanup Old Images -----"
                    # List and sort images by creation time, keeping only the two most recent builds
                    docker images --format "{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedAt}}" | \
                    grep "${DOCKER_IMAGE}" | \
                    sort -k3 -r | \
                    awk 'NR>2 {print $2}' | \
                    xargs -r docker rmi || true
                    
                    echo "===== Deployment Success Cleanup Complete ====="
                '''
            }
        }
    }
}
