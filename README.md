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
