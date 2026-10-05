"""
EyeVerse - AI-Based Eye Disease Detection Web Application
Flask Backend with PyTorch Model
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np
import json
from datetime import datetime
import io
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'static/results'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Disease classifications
CLASS_NAMES = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']

REPORT_TEMPLATES = {
    0: {
        'diagnosis': 'No Diabetic Retinopathy',
        'description': 'No signs of diabetic retinopathy detected. Retina appears healthy with normal blood vessels and no lesions.',
        'recommendations': [
            'Continue annual diabetic eye screening',
            'Maintain optimal blood glucose control (HbA1c < 7%)',
            'Monitor blood pressure regularly',
            'Follow up in 12 months'
        ],
        'severity': 'Normal',
        'color': '#28a745'
    },
    1: {
        'diagnosis': 'Mild Non-Proliferative Diabetic Retinopathy',
        'description': 'Mild diabetic retinopathy detected with few microaneurysms visible. Early stage requiring close monitoring.',
        'recommendations': [
            'Increase screening frequency to every 6-12 months',
            'Optimize glycemic control immediately',
            'Control blood pressure and lipids',
            'Consider specialist referral if progression occurs'
        ],
        'severity': 'Mild',
        'color': '#ffc107'
    },
    2: {
        'diagnosis': 'Moderate Non-Proliferative Diabetic Retinopathy',
        'description': 'Moderate diabetic retinopathy with multiple microaneurysms and dot hemorrhages present. More frequent monitoring needed.',
        'recommendations': [
            'Screening every 3-6 months recommended',
            'Urgent optimization of blood sugar, BP, and lipids',
            'Referral to ophthalmologist for comprehensive evaluation',
            'Consider laser photocoagulation if progressing'
        ],
        'severity': 'Moderate',
        'color': '#fd7e14'
    },
    3: {
        'diagnosis': 'Severe Non-Proliferative Diabetic Retinopathy',
        'description': 'Severe diabetic retinopathy with extensive hemorrhages, venous beading, and intraretinal abnormalities. Immediate specialist consultation required.',
        'recommendations': [
            'IMMEDIATE referral to retinal specialist',
            'Panretinal photocoagulation (PRP) likely indicated',
            'Screening every 2-4 months',
            'Aggressive systemic management essential',
            'High risk of vision loss without intervention'
        ],
        'severity': 'Severe',
        'color': '#dc3545'
    },
    4: {
        'diagnosis': 'Proliferative Diabetic Retinopathy',
        'description': 'Proliferative diabetic retinopathy detected with neovascularization present. Risk of vitreous hemorrhage and retinal detachment. EMERGENCY consultation required.',
        'recommendations': [
            'EMERGENCY referral to ophthalmologist',
            'Urgent laser photocoagulation or anti-VEGF injection',
            'Monthly monitoring required',
            'High risk of severe vision loss',
            'Patient education on warning signs (floaters, vision loss)'
        ],
        'severity': 'Critical',
        'color': '#721c24'
    }
}

# Global model variable
model = None
device = None

def load_model():
    """Load the trained PyTorch model"""
    global model, device
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Loading model on {device}...")
    
    # Build model architecture (must match training)
    model = models.resnet50(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 256),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(256, 5)
    )
    
    # Load trained weights
    model_path = 'models/classifier_best_pytorch.pth'
    if os.path.exists(model_path):
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(device)
        model.eval()
        print("✓ Model loaded successfully!")
        return True
    else:
        print(f"✗ Model not found at {model_path}")
        print("Please ensure the trained model is in the models/ directory")
        return False

def preprocess_image(image_path):
    """Preprocess image for model input"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    
    return image, image_tensor

def predict(image_tensor):
    """Make prediction using the model"""
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_class = outputs.argmax(dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    return predicted_class, confidence, probabilities[0].cpu().numpy()

def generate_report(predicted_class, confidence, probabilities):
    """Generate diagnostic report"""
    template = REPORT_TEMPLATES[predicted_class]
    
    report = {
        'diagnosis': template['diagnosis'],
        'severity': template['severity'],
        'confidence': f"{confidence * 100:.2f}%",
        'confidence_value': confidence * 100,
        'class_id': predicted_class,
        'description': template['description'],
        'recommendations': template['recommendations'],
        'probabilities': {
            CLASS_NAMES[i]: f"{prob * 100:.2f}%" 
            for i, prob in enumerate(probabilities)
        },
        'color': template['color'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return report

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Preprocess and predict
            image, image_tensor = preprocess_image(filepath)
            predicted_class, confidence, probabilities = predict(image_tensor)
            
            # Generate report
            report = generate_report(predicted_class, confidence, probabilities)
            
            # Convert image to base64 for display
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            report['image'] = img_str
            report['filename'] = filename
            
            return jsonify(report)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/help')
def help_page():
    """Help page"""
    return render_template('help.html')

@app.route('/api/model-info')
def model_info():
    """Get model information"""
    info = {
        'model_loaded': model is not None,
        'device': str(device) if device else 'Not loaded',
        'classes': CLASS_NAMES,
        'num_classes': len(CLASS_NAMES)
    }
    return jsonify(info)

if __name__ == '__main__':
    print("="*70)
    print("EyeVerse - AI-Based Eye Disease Detection")
    print("="*70)
    
    # Load model
    if load_model():
        print("\nStarting Flask server...")
        print("Access the application at: http://localhost:5000")
        print("="*70)
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n✗ Failed to load model. Please train the model first.")
        print("Run: python train_pytorch.py")