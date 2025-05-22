pipeline {
    agent any

    environment {
        GITREPO = "https://github.com/thirumalai-py/flask-docker"
        GIT_BRANCH = "main"
        EC2_SSH = "thiru-ec2"
        EC2_USER = "ubuntu"
        EC2_HOST = "13.233.192.172"
        CONTAINER_NAME = "thiru-flask"
        DOCKER_IMAGE = "thirumalaipy/flask"
        DOCKER_CREDENTIALS_ID = "thiru-docker-cred"
        DOCKER_REGISTRY = "https://index.docker.io/v1"
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
                            echo "Starting MongoDB with seed data..."
                            docker-compose up -d mongo-db

                            echo "Waiting for MongoDB to be ready..."
                            # Wait for MongoDB to be fully operational
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
                            echo "Pulling Docker Image..."
                            docker pull ${DOCKER_IMAGE}:${BUILD_NUMBER}

                            echo "Stopping and Removing Existing Container..."
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true

                            echo "Running New Container..."
                            docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${DOCKER_IMAGE}:${BUILD_NUMBER}

                            echo "Deployment Complete!"
                        '
                    """
                }
            }
        }
    }

    post {
        failure {
            echo 'Build or test failed. Sending notifications...'
        }
        success {
            echo 'Build and deployment passed successfully!'
        }
    }
}
