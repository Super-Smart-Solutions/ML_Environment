# ML API Project

This project provides a FastAPI-based API for ML model inference, including image upload and parameterization. The application is designed to be dockerized for easy deployment and scalability.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application Locally](#running-the-application-locally)
- [Running the Application with Docker](#running-the-application-with-docker)
- [Testing the API](#testing-the-api)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or later
- Docker (for containerization)
- Docker Desktop (for Windows or macOS) or Docker Engine (for Linux)

## Project Structure

The project directory is organized as follows:

```
ml_api/
├── app/
│   ├── main.py
│   ├── ml_models/
│   │   ├── ml_model_1.py
│   │   ├── ml_model_2.py
│   │   └── ...
│   ├── utils/
│   │   ├── preprocessing.py
│   │   └── postprocessing.py
│   ├── schemas/
│   │   ├── request.py
│   │   └── response.py
│   └── api/
│       ├── inference.py
│       └── healthcheck.py
├── Dockerfile
├── requirements.txt
└── README.md
```

- **`app/main.py`**: The main FastAPI application file.
- **`app/ml_model_1.py`**: Mock model for inference.
- **`app/ml_model_2.py`**: Another mock model for inference.
- **`requirements.txt`**: List of Python dependencies.
- **`Dockerfile`**: Dockerfile for containerizing the application.

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd your_project
   ```

2. **Install Python Dependencies**

   Create a virtual environment (optional but recommended) and install the dependencies:

   ```bash
   python -m venv ML_API
   source ML_API/bin/activate  # On Windows use `ML_API\Scripts\activate`
   pip install -r requirements.txt
   ```

## Running the Application Locally

1. **Run the FastAPI Application**

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be available at `http://localhost:8000`.

## Running the Application with Docker

1. **Build the Docker Image**

   Navigate to the project directory and build the Docker image:

   ```bash
   docker build -t ml_api .
   ```

2. **Run the Docker Container**

   Run the Docker container, mapping port 8000:

   ```bash
   docker run -d -p 8000:8000 ml_api:latest
   ```

   If port 8000 is already in use, you can use a different port:

   ```bash
   docker run -d -p 8001:8000 ml_api
   ```

   The application will be available at `http://localhost:8000` (if you used port 8000).

## Testing the API

1. **Access Swagger UI**

   Open your browser and navigate to `http://localhost:8000/docs` to access the Swagger UI for interactive API testing.

2. **Use Curl or Postman**

   You can also test the API endpoints using `curl` or Postman:

   - **Using Curl**:

     ```bash
     curl -X POST "http://localhost:8000/inference" -F "file=@path_to_your_image.jpg" -F "model_name=ml_model_1"
     ```

   - **Using Postman**:

     - Set the method to `POST`.
     - URL: `http://localhost:8000/inference`.
     - Add a form-data field with `file` as the key and your image as the value.
     - Add another form-data field with `model_name` as the key and `model_1` or `model_2` as the value.


