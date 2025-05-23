# Flask User Management API with MongoDB

## Project Setup

### Prerequisites
- Python 3.8+
- MongoDB
- pip

### Installation Steps

1. Clone the repository
```bash
git clone <your-repo-url>
cd flask-docker
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up MongoDB
- Ensure you have a MongoDB instance running
- Set the `MONGO_URI` environment variable with your MongoDB connection string

5. Set Environment Variables
Create a `.env` file with the following content:
```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/
JWT_SECRET_KEY=your-very-secret-key-that-should-be-long-and-random
FLASK_ENV=development
```

6. Run Database Migrations
```bash
flask db upgrade
```

7. Run the Application
```bash
python app.py
```

### API Endpoints

- `POST /register`: User registration
- `POST /login`: User login (returns JWT token)
- `GET /profile`: Get user profile (requires JWT)
- `PUT /profile`: Edit user profile (requires JWT)
- `POST /change-password`: Change user password (requires JWT)
- `POST /logout`: Logout user (client-side token removal)

### Authentication
- Use JWT token in Authorization header for protected routes
- Token format: `Authorization: Bearer <your_token>`

### Testing
- Use tools like Postman or curl to test the API endpoints
- Ensure you have a valid JWT token for protected routes

### MongoDB Configuration
- The application uses PyMongo for MongoDB interactions
- Connection details are managed through environment variables
- Supports both local and cloud MongoDB instances

## Running Tests

### Prerequisites
- Python 3.8+
- MongoDB
- pip

### Setup
1. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
To run all tests:
```bash
pytest
```

To run specific test files:
```bash
# Run authentication tests
pytest tests/test_auth.py

# Run profile tests
pytest tests/test_profile.py
```

### Test Coverage
- Authentication tests cover:
  - User registration
  - Login
  - Invalid login scenarios
- Profile tests cover:
  - Retrieving profile
  - Updating profile
  - Changing password
  - Unauthorized access checks

### Notes
- Tests use a separate test database
- Test data is automatically cleaned up after each test run

## Jenkins CI/CD Pipeline Overview

This project implements a comprehensive Continuous Integration and Continuous Deployment (CI/CD) pipeline using Jenkins, demonstrating a robust automated workflow for a Flask application.

### Pipeline Stages

#### 1. Get Build Number
- Captures and logs the unique build number for tracking and identification

#### Output
This screenshot illustrates the first stage of the Jenkins pipeline, which captures and logs the unique build number. The build number serves as a critical identifier for tracking each specific build and deployment iteration.

![Get Build Number Stage](/outputs/1_get_build_no.png)

#### 2. Checkout Code
- Pulls the latest code from the main branch of the GitHub repository

#### Output
This screenshot demonstrates the Checkout Code stage, where Jenkins pulls the latest code from the main branch of the GitHub repository. This ensures that the most recent version of the codebase is used for building, testing, and deployment.

![Checkout Code Stage](/outputs/2_checkout_code.png)

#### 3. Run Tests
- Sets up a MongoDB container with seed data
- Runs pytest with the following characteristics:
  - Generates XML test reports
  - Stops on first test failure
  - Captures and reports test results
- Ensures clean environment by tearing down containers after testing

#### Output - Successful Test
This screenshot shows a successful test run, demonstrating that all tests passed. The green indicators and test report confirm the application's functionality and code quality.

![Run Tests Stage - Success](/outputs/3_run_test.png)

#### Output - Successful Test Report

![Test Results Report](/outputs/test_results.png)


#### Output - Failed Tests
This screenshot illustrates a test failure scenario, highlighting the importance of comprehensive testing. When tests fail, the Jenkins pipeline provides detailed error messages and stack traces to help developers quickly identify and resolve issues.

![Run Tests Stage - Failure](/outputs/test_failure.png)

#### 4. Build Docker Image
- Builds a Docker image for the Flask application
- Tags the image with the current build number

#### Output
This screenshot captures the Docker image build stage, where a Docker image is created for the Flask application. The build process compiles the application, installs dependencies, and packages the entire application into a portable, reproducible container.

![Build Docker Image Stage](/outputs/4_build_docker.png)

#### 5. Test Docker Credentials
- Validates Docker Hub credentials
- Ensures secure authentication for image push and pull operations

#### Output
This screenshot demonstrates the Docker credentials testing stage, which validates the Docker Hub authentication credentials. This critical security step ensures secure and authorized access to Docker Hub for pushing and pulling container images.

![Test Docker Credentials Stage](/outputs/5_test_docker.png)

#### 6. Push Docker Image
- Pushes the built Docker image to Docker Hub
- Uses secure credential management

#### Output
This screenshot illustrates the Push Docker Image stage, where the newly built Docker image is securely uploaded to Docker Hub. This step ensures that the latest version of the application is available for deployment and can be easily pulled by other systems or team members.

![Push Docker Image Stage](/outputs/6_push_docker.png)

#### 7. Deploy to EC2
- Connects to a predefined EC2 instance via SSH
- Creates/checks Docker network and volumes
- Ensures MongoDB container is running
- Pulls the latest Docker image
- Stops and removes any existing container
- Starts a new container with:
  - Proper network configuration
  - Environment variables
  - Port mapping

#### Output
This screenshot depicts the Deploy to EC2 stage, which demonstrates the automated deployment process to the target EC2 instance. The image shows the successful SSH connection, Docker image pull, and container startup, highlighting the seamless and reproducible deployment workflow.

![Deploy to EC2 Stage](/outputs/7_deploy_ec2.png)

### Notification System
- Sends email notifications for:
  - Build failures
  - Successful deployments

### Post-Deployment Actions
- Generates a detailed deployment success summary
- Includes information about:
  - Docker images
  - Running containers
  - Disk space
  - Docker system info
- Performs cleanup by removing older Docker images

#### Output - Clean the Docker images

This screenshot shows the Docker image cleanup stage, which is an essential part of maintaining a clean and efficient Docker environment. After successful deployment, the pipeline removes older Docker images to prevent disk space accumulation and keep the system optimized.

![Clean Docker Images Stage](/outputs/8_post_clean_image.png)

#### Output - Send Email

This screenshot illustrates the email notification sent after a successful deployment. The email provides a comprehensive summary of the build and deployment process, including:

- Job Name
- Build Number
- Git Branch
- Repository URL
- Docker Image Details
- Deployment Target (EC2 Host)
- Deployment Timestamp

The email uses a clean, HTML-formatted layout with color-coded status indicators (green checkmark ✅) to quickly communicate the successful deployment. It includes a direct link to the full build logs, allowing team members to easily access detailed information about the deployment.

This automated notification system ensures that all stakeholders are immediately informed about the deployment status, promoting transparency and quick communication within the development team.

![Send Email Notification](/outputs/email_success.png)

### Environment Variables
Key environment variables used in the pipeline:
- `GITREPO`: Source code repository
- `EC2_HOST`: Deployment target EC2 instance
- `DOCKER_IMAGE`: Docker image name
- `CONTAINER_NAME`: Name of the deployed container
- `ALERT_EMAIL`: Notification email address

### Prerequisites
- Jenkins
- Docker
- Docker Compose
- EC2 Instance
- Docker Hub Account

### Deployment Workflow
1. Code is pushed to the main branch
2. Jenkins automatically triggers the pipeline
3. Tests are run
4. Docker image is built and pushed
5. Application is deployed to EC2
6. Notifications are sent

## Local Development
Refer to the `docker-compose.yml` for local setup instructions.

## Contributing
Please read the contributing guidelines before submitting pull requests.
