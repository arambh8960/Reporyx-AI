# Reporyx-AI - Backend

AI-Powered Developer Onboarding Assistant for GitHub Repositories

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Motor** - Async MongoDB driver
- **Python-JOSE** - JWT token handling
- **Passlib** - Password hashing
- **Pydantic** - Data validation

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `MONGODB_URL` - MongoDB connection string
- `JWT_SECRET_KEY` - Secret key for JWT (use a strong random string in production)
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_EXPIRE_MINUTES` - JWT token expiration time in minutes

## MongoDB Setup

1. Install MongoDB:
   - **Mac**: `brew install mongodb-community`
   - **Ubuntu**: `sudo apt-get install mongodb`
   - **Windows**: Download from [MongoDB官网](https://www.mongodb.com/try/download/community)

2. Start MongoDB:
```bash
# Mac/Linux
mongod --config /usr/local/etc/mongod.conf

# Or use system service
brew services start mongodb-community  # Mac
sudo systemctl start mongod  # Linux
```

3. Verify MongoDB is running:
```bash
mongosh
```

## Running the Backend

1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health
- `GET /api/health` - Health check endpoint

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login

## Authentication Flow

1. **Signup**: User provides name, email, and password
   - Password is hashed using bcrypt
   - User is stored in MongoDB
   - Returns success message

2. **Login**: User provides email and password
   - Credentials are validated
   - JWT token is generated
   - Returns access token

3. **Protected Routes**: Include JWT token in Authorization header
   ```
   Authorization: Bearer <access_token>
   ```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── routes/              # API route handlers
│   ├── auth.py         # Authentication endpoints
│   └── health.py       # Health check endpoint
├── services/            # Business logic
│   ├── auth_service.py # Authentication service
│   └── jwt_service.py  # JWT token service
├── database/            # Database configuration
│   └── mongo_db.py     # MongoDB connection
├── schemas/             # Pydantic schemas
│   ├── auth_schema.py  # Authentication schemas
│   └── token_schema.py # Token schemas
├── models/              # Database models
│   └── user_model.py   # User model
└── utils/               # Utility functions
    ├── password.py     # Password hashing utilities
    └── dependencies.py # FastAPI dependencies
```

## Development

The backend uses async/await patterns with Motor for MongoDB operations. All database operations are non-blocking.

## Security Notes

- Never commit `.env` file to version control
- Use strong JWT secret keys in production
- Implement rate limiting for production
- Use HTTPS in production
- Validate all input data
