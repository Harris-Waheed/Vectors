# The Vectors - FastAPI Backend

## Overview
This is the backend API for The Vectors, an e-commerce platform specializing in wooden decorative frames. Built with FastAPI, this application handles the core business logic, product catalog management, and seamless operations for the store.

## Features
* RESTful API architecture built with FastAPI
* Product and inventory management
* Fast, asynchronous request handling
* Automatic interactive API documentation

## Prerequisites
* Python 3.8 or higher
* pip (Python package installer)

## Installation

1. Clone the repository:
   git clone <your-repository-url>
   cd <your-project-directory>

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

4. Install the required dependencies:
   pip install -r requirements.txt

## Running the Application

To start the development server, run the following command in your terminal:

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can explore and test the endpoints by navigating to:
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Project Structure
* `main.py`: The entry point of the FastAPI application.
* `models/`: Database models and schemas.
* `routes/`: API endpoint definitions.
* `database.py`: Database connection and configuration.
