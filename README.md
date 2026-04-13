# Wound Healing Tracker

A FastAPI-based backend system for tracking wound healing progress using AI-powered image analysis. The system uses a U-Net model to analyze wound images, detect wound areas, and monitor healing progress over time.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Wound Management**: Create and manage wound records for patients
- **AI-Powered Analysis**: Upload wound images for automatic segmentation and area calculation
- **Healing Progress Tracking**: Monitor wound healing over time with metrics
- **Analytics Dashboard**: Get wound progress statistics and visualizations
- **Image Processing**: Automatic generation of masks and overlays for wound visualization

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: TensorFlow/Keras with U-Net model
- **Image Processing**: OpenCV, Pillow, NumPy
- **Authentication**: JWT tokens with python-jose
- **Migrations**: Alembic

## Project Structure

```
app/
├── core/               # Core configuration (security, dependencies)
├── db/                 # Database models and session management
│   ├── models/         # SQLAlchemy models (User, Wound, WoundRecord)
│   └── base.py         # Base model configuration
├── ml/                 # Machine learning components
│   ├── model.py        # Model loading and management
│   ├── preprocess.py   # Image preprocessing
│   └── postprocess.py  # Mask postprocessing
├── routes/api/         # API endpoints
│   ├── auth.py         # Authentication routes
│   ├── user.py         # User management
│   ├── wounds.py       # Wound CRUD operations
│   ├── records.py      # Wound record upload and retrieval
│   ├── ai.py           # AI prediction endpoints
│   └── analytic.py     # Analytics and progress tracking
├── services/           # Business logic layer
│   ├── auth_service.py
│   ├── wound_service.py
│   ├── ai_service.py   # ML prediction logic
│   ├── ml_pipeline.py  # Area processing and smoothing
│   └── analytics_service.py
├── utils/              # Utility functions
│   ├── image.py        # Image processing utilities
│   ├── storage.py      # File storage handling
│   └── response.py     # Response formatting
└── main.py             # Application entry point
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### User Management
- `GET /user/me` - Get current user profile
- `PUT /user/me` - Update user profile

### Wounds
- `POST /wounds/` - Create new wound record
- `GET /wounds/` - List user's wounds
- `GET /wounds/{id}` - Get specific wound details

### Records
- `POST /records/wounds/{wound_id}` - Upload wound image for analysis
- `GET /records/wounds/{wound_id}` - Get all records for a wound
- `GET /records/wounds/{wound_id}/predict` - Get prediction without saving

### AI Analysis
- `POST /ai/predict` - Predict wound area from image

### Analytics
- `GET /analytics/wounds/{wound_id}/progress` - Get healing progress data

## Setup Instructions

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Wound Healing System"
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost/wound_healing"
export SECRET_KEY="your-secret-key"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

5. Run database migrations:
```bash
cd app
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Model Information

The system uses a U-Net model trained for wound segmentation:
- **Input**: 256x256 RGB images
- **Output**: Binary mask indicating wound area
- **Preprocessing**: Images are resized maintaining aspect ratio with padding
- **Postprocessing**: Masks are extracted and scaled to original image dimensions

## File Storage

Uploaded files are stored in the following directories:
- `storage/uploads/` - Original uploaded images
- `storage/masks/` - Generated wound masks
- `storage/overlays/` - Overlay images with wound highlighting
- `media/` - Temporary processing files

## Key Features

### Aspect Ratio Preservation
The system maintains image aspect ratios during preprocessing to ensure accurate wound location mapping in overlays.

### Area Smoothing
Implements Exponential Moving Average (EMA) to smooth area calculations and reduce noise from prediction variations.

### Healing Percentage Calculation
Tracks healing progress by comparing current wound area against baseline (first measurement).

## CORS Configuration

The API is configured with CORS enabled to allow cross-origin requests from any origin during development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```