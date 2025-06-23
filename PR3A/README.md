# Real-Time Apple Detection System

A Raspberry Pi-based computer vision system that uses YOLOv11 neural network to detect and classify apples in real-time through a camera feed. The system provides live video analysis with confidence scoring and visual feedback, making it ideal for agricultural applications, quality control, or research purposes.

## Features

- **Real-time object detection** using YOLOv11 neural network
- **High-accuracy apple classification** with confidence scoring
- **Live camera feed processing** with Picamera2 integration
- **Visual feedback system** with on-screen detection labels
- **Confidence threshold filtering** (70% minimum for reliable detection)
- **Optimized performance** for Raspberry Pi hardware
- **Graceful shutdown** with proper resource cleanup
- **Custom model support** with easy model replacement

## Hardware Requirements

### Components

- Raspberry Pi 4 (recommended for optimal performance)
- Raspberry Pi Camera Module (v2 or v3 recommended)
- MicroSD card (32GB+ recommended)
- External monitor or display
- Keyboard for system control

### Camera Setup

| Component | Connection | Notes |
|-----------|------------|-------|
| Pi Camera Module | CSI connector | Connect to camera port on Raspberry Pi |
| Display | HDMI | For viewing detection results |
| Power | USB-C | Ensure adequate power supply |

## Software Requirements

### System Requirements

- Raspberry Pi OS
- Python 3.8+
- Camera interface enabled
- Sufficient RAM (4GB+ recommended for YOLOv11)

### Dependencies

- `cv2` (OpenCV)
- `picamera2`
- `ultralytics` (YOLO)
- `time`
- `numpy`

## Installation

1. **Enable Camera Interface**
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > Camera > Enable
   ```

2. **Clone or download the project files**
   ```bash
   git clone https://github.com/EVTA-EU/AISVE.git
   cd AISVE/PR3B
   ```

3. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Verify camera functionality**
   ```bash
   libcamera-hello
   # Should display camera preview
   ```

5. **Place the trained model** in the `model/` directory (see Model Training section)

## Model Training

The YOLOv11 apple detection model is trained using a comprehensive Jupyter notebook located in the `model/` directory. This notebook implements a complete step-by-step training pipeline including:

- **Dataset preparation**
- **YOLOv11 model configuration**
- **Training process**
- **Validation and testing procedures**
- **Model export and optimization**
- **Performance evaluation metrics**

### Training Setup

**Recommended Environment:**
- **Google Colab with GPU acceleration** (strongly recommended)
- **Minimum 6GB GPU memory** for optimal training
- **High-speed internet** for dataset downloading

**Training Process:**
1. Open `model/yolov11_apple_training.ipynb` in Google Colab
2. Enable GPU runtime (Runtime > Change runtime type > GPU)
3. Follow the step-by-step instructions in the notebook
4. Download the trained model (`yolov11_apple.pt`) when complete
5. Place the model file in your Raspberry Pi's `model/` directory

**Training Features:**
- Custom dataset preparation for apple detection
- Data augmentation techniques for improved robustness
- Transfer learning from pre-trained YOLOv11 weights
- Comprehensive evaluation metrics and visualizations
- Model optimization for deployment

## Usage

### Running the Detection System

```bash
python main.py
```

### System Operation

The system operates in real-time once started:

1. **Camera Initialization**: Picamera2 starts with 800x600 resolution
2. **Model Loading**: YOLOv11 model loads for inference
3. **Live Detection**: Continuous frame processing and analysis
4. **Result Display**: Best detection shown with confidence score
5. **Visual Feedback**: Detection labels overlaid on video feed

### Stopping the System

Press the `q` key in the video window to gracefully shutdown the detection system.

## System Behavior

### Detection Logic

| Condition | Confidence Score | Display Action |
|-----------|-----------------|----------------|
| Apple detected | ≥ 70% | 🍎 **Label with confidence** |
| Apple detected | < 70% | 📱 No display (filtered out) |
| No apple | N/A | 📱 Clean video feed |

### Detection States

- **Active Detection**: Red text overlay showing "apple XX.XX%" for valid detections
- **Confidence Filtering**: Only detections above 70% confidence are displayed
- **Best Match Selection**: When multiple apples detected, shows highest confidence
- **Real-time Processing**: Continuous analysis at camera frame rate

### Status Information

| Console Output | Meaning | Description |
|----------------|---------|-------------|
| Camera preview | System Ready | Camera initialized successfully |
| Model loading | AI Ready | YOLOv11 model loaded and ready |
| Live video feed | Active Detection | Real-time processing in progress |
| Detection labels | Apple Found | Visual confirmation of detection |

## Configuration

### Customizable Parameters

Edit the following variables in `main.py`:

```python
# Camera Configuration
CAMERA_WIDTH = 800          # Camera resolution width
CAMERA_HEIGHT = 600         # Camera resolution height
CAMERA_FORMAT = "RGB888"    # Color format

# Detection Parameters
CONFIDENCE_THRESHOLD = 70.0  # Minimum confidence (%)
MODEL_PATH = "model/yolov11_apple.pt"  # Model location

# Display Configuration
FONT_SCALE = 1.5            # Text size
FONT_COLOR = (0, 0, 255)    # Text color (BGR - Red)
FONT_THICKNESS = 3          # Text thickness
TEXT_POSITION = (30, 60)    # Label position (x, y)
```

### Performance Tuning

```python
# Model optimization (if needed)
# Note: Avoid NCNN export for best compatibility
model = YOLO("model/yolov11_apple.pt")

# Camera optimization
picam2.preview_configuration.main.size = (640, 480)  # Lower resolution for speed
```

## Troubleshooting

### Common Issues

**Camera Not Working**
```bash
# Check camera detection
vcgencmd get_camera
# Should return "supported=1 detected=1"

# Test camera functionality
libcamera-hello --timeout 5000
```

**Model Loading Errors**
- Verify model file exists in `model/yolov11_apple.pt`
- Check model file integrity (not corrupted)
- Ensure sufficient RAM available
- Try restarting the system

**Poor Detection Performance**
- Ensure good lighting conditions
- Check camera focus and cleanliness
- Verify apple visibility in frame
- Consider retraining model with your specific apple varieties

**Low Frame Rate**
```python
# Reduce resolution for better performance
picam2.preview_configuration.main.size = (640, 480)
```

**Memory Issues**
```bash
# Check available memory
free -h

# Increase swap space if needed
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

**Import Errors**
```bash
# Update package list
sudo apt update

# Install missing dependencies
pip install --upgrade ultralytics
pip install --upgrade opencv-python
```

### Debug Mode

Add debug information for troubleshooting:

```python
# Add after model loading
print(f"Model loaded: {model}")
print(f"Model classes: {model.names}")

# Add in detection loop
print(f"Detection confidence: {confidence:.2f}%")
print(f"Detected class: {best_label}")
```

### Hardware Testing

**Test Individual Components:**

```bash
# Test camera
libcamera-still -o test.jpg

# Check Python imports
python -c "import cv2, picamera2, ultralytics; print('All imports successful')"

# Monitor system resources
htop
```

## Performance Optimization

This detection system is optimized for:

- **Real-time Processing**: Efficient frame processing pipeline
- **Resource Management**: Optimized memory usage for Raspberry Pi
- **Accuracy Balance**: High confidence threshold for reliable detection
- **Hardware Compatibility**: Designed for Raspberry Pi 4 performance
- **Model Efficiency**: YOLOv11 provides excellent speed/accuracy balance

## Applications

- **Agricultural Monitoring**: Automated crop assessment and quality control
- **Harvest Automation**: Integration with robotic picking systems
- **Quality Inspection**: Real-time fruit grading and sorting
- **Research Applications**: Agricultural AI research and development
- **Educational Projects**: Computer vision and AI learning platform
- **Smart Farming**: IoT integration for precision agriculture
- **Food Processing**: Automated inspection in processing facilities

## Safety Considerations

- **Electrical Safety**: Ensure proper power supply and grounding
- **Camera Positioning**: Secure mounting to prevent damage
- **Environmental Protection**: Consider weatherproofing for outdoor use
- **System Monitoring**: Regular performance checks and maintenance

## Model Performance

- **Training Dataset**: Custom apple dataset with diverse varieties and conditions
- **Accuracy**: >90% precision on validation set
- **Speed**: Real-time inference on Raspberry Pi 4
- **Robustness**: Trained with various lighting and background conditions
- **Confidence Scoring**: Reliable probability estimates for detection quality

## Future Enhancements

- Multi-fruit detection capabilities
- Apple variety classification
- Size estimation and quality assessment
- Integration with IoT platforms
- Mobile app connectivity
- Cloud-based model updates
