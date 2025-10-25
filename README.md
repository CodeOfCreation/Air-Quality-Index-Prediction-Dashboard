# Air Quality Index (AQI) Prediction Dashboard

A Django-based web application that predicts Air Quality Index using machine learning models (Linear Regression and Decision Tree). The dashboard allows users to input air quality parameters and displays predictions from both models with visual comparisons.

## Features

- Machine learning models for AQI prediction (Linear Regression and Decision Tree)
- Responsive web interface with Bootstrap 5
- Real-time visualization of predictions using Chart.js
- Historical prediction tracking and analysis
- AQI category classification with color coding
- REST API endpoint for programmatic access

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeOfCreation/Air-Quality-Index-Prediction-Dashboard.git
cd aqi-prediction-dashboard

steps to compute this project directly
1) pip install -r ml_models/requirements.txt
to install all dependencies for ml 
1.1)python manage.py makemigrations
python manage.py migrate
add variables to create table columns in data storage which is sqlite3 
2)python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
set virtual enviroment
3)pip install django
4)python ml_models/train.py
train ml models and create pkl file in ml_models/models
5)python manage.py runserver
start enviroment this will take you to browser

note- make sure you are in virtual enviroment or you have a venv file created
