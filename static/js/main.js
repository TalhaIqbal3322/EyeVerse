// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage');
const uploadPlaceholder = document.querySelector('.upload-placeholder');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const downloadReportBtn = document.getElementById('downloadReportBtn');

let selectedFile = null;

// Upload Area Click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File Input Change
fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
});

// Handle File Selection
function handleFileSelect(file) {
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file (JPG, PNG, etc.)');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        uploadPlaceholder.style.display = 'none';
        analyzeBtn.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Analyze Button Click
analyzeBtn.addEventListener('click', () => {
    if (!selectedFile) return;
    
    // Hide analyze button, show loading
    analyzeBtn.style.display = 'none';
    loadingSpinner.style.display = 'block';
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Send to backend
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingSpinner.style.display = 'none';
        
        if (data.error) {
            alert('Error: ' + data.error);
            analyzeBtn.style.display = 'block';
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        loadingSpinner.style.display = 'none';
        analyzeBtn.style.display = 'block';
        alert('Error analyzing image: ' + error.message);
    });
});

// Display Results
function displayResults(data) {
    // Scroll to results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Set image
    document.getElementById('resultImage').src = 'data:image/png;base64,' + data.image;
    document.getElementById('imageInfo').innerHTML = `
        <strong>Filename:</strong> ${data.filename}<br>
        <strong>Analysis Time:</strong> ${data.timestamp}
    `;
    
    // Set diagnosis
    document.getElementById('diagnosisName').textContent = data.diagnosis;
    document.getElementById('severityBadge').textContent = data.severity;
    document.getElementById('severityBadge').style.backgroundColor = data.color;
    
    // Set confidence
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceText = document.getElementById('confidenceText');
    confidenceFill.style.width = data.confidence;
    confidenceText.textContent = data.confidence;
    
    // Set detailed report
    document.getElementById('detailedReport').innerHTML = `
        <p><strong>Clinical Findings:</strong></p>
        <p>${data.description}</p>
    `;
    
    // Set probability chart
    const probabilityChart = document.getElementById('probabilityChart');
    probabilityChart.innerHTML = '';
    
    Object.entries(data.probabilities).forEach(([className, prob]) => {
        const probValue = parseFloat(prob);
        const probBar = document.createElement('div');
        probBar.className = 'prob-bar';
        probBar.innerHTML = `
            <span class="prob-label">${className}</span>
            <div class="prob-bar-container">
                <div class="prob-bar-fill" style="width: ${probValue}%"></div>
            </div>
            <span class="prob-value">${prob}</span>
        `;
        probabilityChart.appendChild(probBar);
    });
    
    // Set recommendations
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
    
    // Store data for download
    window.currentReport = data;
}

// New Analysis Button
newAnalysisBtn.addEventListener('click', () => {
    // Reset everything
    selectedFile = null;
    fileInput.value = '';
    previewImage.style.display = 'none';
    uploadPlaceholder.style.display = 'block';
    analyzeBtn.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Scroll to upload
    document.querySelector('.upload-section').scrollIntoView({ behavior: 'smooth' });
});

// Download Report Button
downloadReportBtn.addEventListener('click', () => {
    if (!window.currentReport) return;
    
    const data = window.currentReport;
    
    // Create text report
    let reportText = `
╔══════════════════════════════════════════════════════════════════╗
║              DIABETIC RETINOPATHY ANALYSIS REPORT                ║
╚══════════════════════════════════════════════════════════════════╝

DIAGNOSIS: ${data.diagnosis}
SEVERITY: ${data.severity}
CONFIDENCE: ${data.confidence}
ANALYSIS DATE: ${data.timestamp}

════════════════════════════════════════════════════════════════════

CLINICAL FINDINGS:
${data.description}

════════════════════════════════════════════════════════════════════

CLASS PROBABILITIES:
`;
    
    Object.entries(data.probabilities).forEach(([className, prob]) => {
        reportText += `  ${className}: ${prob}\n`;
    });
    
    reportText += `
════════════════════════════════════════════════════════════════════

CLINICAL RECOMMENDATIONS:
`;
    
    data.recommendations.forEach((rec, index) => {
        reportText += `  ${index + 1}. ${rec}\n`;
    });
    
    reportText += `
════════════════════════════════════════════════════════════════════

DISCLAIMER:
This is an AI-assisted analysis for educational purposes. Final 
diagnosis should be confirmed by a qualified ophthalmologist. Do not 
use as a substitute for professional medical advice.

════════════════════════════════════════════════════════════════════

Generated by EyeVerse - AI-Based Eye Disease Detection System
Air University Islamabad | Deep Learning Lab Project
Students: Talha Iqbal (231223), Isfah Anmol (231207)
Instructor: Ms. Bismah Malik

════════════════════════════════════════════════════════════════════
`;
    
    // Create download link
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `DR_Report_${data.timestamp.replace(/[: ]/g, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
});

// Check model status on page load
window.addEventListener('load', () => {
    fetch('/api/model-info')
        .then(response => response.json())
        .then(data => {
            if (!data.model_loaded) {
                console.warn('Model not loaded!');
                // You could show a warning banner here
            }
        })
        .catch(error => {
            console.error('Error checking model status:', error);
        });
});