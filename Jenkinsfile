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
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Get Build Number') { 
            steps {
                sh '''
                    echo "Build Number: ${BUILD_NUMBER}"
                '''
            }
        }

        stage('Checkout Code') { 
            steps {
                git branch: "${GIT_BRANCH}", url: "${GITREPO}"
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    sh '''
                        python3 --version
                        which python3
                        python3 -m venv ${VENV_NAME}
                        . ${VENV_NAME}/bin/activate
                        python --version
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        pip install pytest
                        pytest test_app.py --maxfail=1 --disable-warnings --junitxml=test-reports/test-results.xml
                    '''
                }
            }
            post {
                always {
                    junit 'test-reports/*.xml'
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

        stage('Push Docker Image'){
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
        cleanup {
            script {
                sh '''
                    rm -rf ${VENV_NAME}
                '''
            }
        }
    }
}