# EyeVerse - AI-Based Diabetic Retinopathy Detection

EyeVerse is an AI-based deep learning project for detecting and classifying diabetic retinopathy from retinal fundus images.

The project provides a Flask-based web interface where a user can upload a retinal image and receive an AI-based prediction with confidence information and a diagnostic report.

---

## Project Overview

EyeVerse focuses on automated diabetic retinopathy detection using deep learning and computer vision.

### Main Functions

- Detect diabetic retinopathy from retinal fundus images
- Classify images into 5 diabetic retinopathy severity levels
- Display prediction results and confidence scores
- Generate diagnostic information
- Provide a web-based interface for image analysis

---

## Academic Information

| Field | Information |
|---|---|
| Course | AI Project Design and Development (AI-316) |
| Institution | Air University, Islamabad |
| Faculty | Faculty of Computing & AI |
| Department | Department of Creative Technologies |
| Instructor | Farhan Zafar |
| Student / Developer | Talha Iqbal |
| Student ID | 231223 |
| Project Type | Individual Project |

---

## Objectives

The main objectives of EyeVerse are:

1. Develop an AI-based system for diabetic retinopathy detection.
2. Apply deep learning to retinal fundus images.
3. Classify diabetic retinopathy into five severity levels.
4. Develop a simple web interface for image submission and prediction.
5. Display prediction results in an understandable format.
6. Organize the project using a structured AI engineering workflow.

---

## Features

### AI Model

- Multi-class diabetic retinopathy classification
- Five severity classes
- Transfer learning using ResNet50
- PyTorch-based deep learning model
- Confidence-based prediction

### Web Application

- Flask backend
- Responsive web interface
- Retinal image upload
- Image preview
- Prediction results
- Confidence information
- Diagnostic report generation

### Project Development

- Structured dataset directories
- Separate source code directory
- Model storage
- Configuration directory
- Notebook directory
- Log directory
- Python virtual environment
- Git-ready project structure

---

## Diabetic Retinopathy Classes

The model classifies retinal images into five categories:

| Class | Description |
|---|---|
| 0 | No Diabetic Retinopathy |
| 1 | Mild Diabetic Retinopathy |
| 2 | Moderate Diabetic Retinopathy |
| 3 | Severe Diabetic Retinopathy |
| 4 | Proliferative Diabetic Retinopathy |

---

## Technology Stack

### Programming Language

- Python

### Deep Learning

- PyTorch
- torchvision
- ResNet50

### Backend

- Flask

### Frontend

- HTML5
- CSS3
- JavaScript
- Font Awesome

### AI / Computer Vision

- OpenCV
- NumPy
- Matplotlib

### Development Tools

- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code

---

## Dataset

The project uses retinal fundus images for diabetic retinopathy classification.

### Dataset

APTOS 2019 Blindness Detection

### Dataset Information

- Retinal fundus images
- Five diabetic retinopathy classes
- Used for deep learning classification

The dataset should be placed inside the appropriate project data directories.

---

## Project Structure

```text
Eyeverse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── classifier_best_pytorch.pth
│
├── notebooks/
│
├── src/
│
├── configs/
│
├── logs/
│
├── static/
│
├── templates/
│   ├── index.html
│   ├── about.html
│   └── help.html
│
├── uploads/
│
├── aipdd_env/
│
├── app.py
├── requirements.txt
├── .gitignore
└── readme.md