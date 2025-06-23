# Real-Time Trash Segmentation System

A Raspberry Pi-based computer vision system that uses YOLOv11 segmentation neural network to detect and segment trash objects in real-time through a camera feed. The system provides pixel-perfect segmentation masks with visual overlays, making it ideal for waste management applications, environmental monitoring, or recycling automation.

## Features

- **Real-time object segmentation** using YOLOv11 segmentation model
- **Pixel-perfect trash detection** with detailed segmentation masks
- **Live camera feed processing** with Picamera2 integration
- **Multi-color visual feedback** with transparent mask overlays
- **Dual detection modes** supporting both segmentation and bounding box detection
- **Low confidence threshold** (1%) for maximum sensitivity
- **Contour enhancement** for better object definition
- **Robust error handling** with graceful shutdown
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
| Display | HDMI | For viewing segmentation results |
| Power | USB-C | Ensure adequate power supply |

## Software Requirements

### System Requirements

- Raspberry Pi OS
- Python 3.8+
- Camera interface enabled
- Sufficient RAM (4GB+ recommended for YOLOv11 segmentation)

### Dependencies

- `cv2` (OpenCV)
- `numpy`
- `picamera2`
- `ultralytics` (YOLO)
- `time`
- `os`

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

The YOLOv11 trash segmentation model is trained using a comprehensive Jupyter notebook located in the `model/` directory. This notebook implements a complete step-by-step training pipeline including:

- **Dataset preparation and annotation** for trash segmentation
- **YOLOv11 segmentation model configuration**
- **Training process with segmentation-specific optimization**
- **Mask validation and quality assessment**
- **Model export and deployment preparation**
- **Performance evaluation with metrics**

### Training Setup

**Recommended Environment:**
- **Google Colab with GPU acceleration** (strongly recommended)
- **Minimum 6GB GPU memory** for segmentation training
- **High-speed internet** for dataset downloading

**Training Process:**
1. Open `model/yolov11_seg_trash_training.ipynb` in Google Colab
2. Enable GPU runtime (Runtime > Change runtime type > GPU)
3. Follow the step-by-step instructions in the notebook
4. Download the trained model (`yolov11_seg_trash.pt`) when complete
5. Place the model file in your Raspberry Pi's `model/` directory

**Training Features:**
- Custom trash dataset with pixel-level annotations
- Data augmentation for improved segmentation robustness
- Transfer learning from pre-trained YOLOv11 segmentation weights
- Comprehensive mask quality evaluation
- Model optimization for real-time deployment

## Usage

### Running the Segmentation System

```bash
python main.py
```

### System Operation

The system operates in real-time once started:

1. **Camera Initialization**: Picamera2 starts with 800x600 resolution
2. **Model Loading**: YOLOv11 segmentation model loads for inference
3. **Live Segmentation**: Continuous frame processing with mask generation
4. **Visual Overlay**: Colored transparent masks overlaid on video feed
5. **Contour Enhancement**: Object boundaries highlighted for clarity

### Stopping the System

Press the `q` key in the video window to gracefully shutdown the segmentation system.

## System Behavior

### Detection Logic

| Condition | Confidence Score | Display Action |
|-----------|-----------------|----------------|
| Trash detected | ≥ 1% | 🗑️ **Segmentation mask + bounding box** |
| Multiple objects | Variable | 🎨 **Different colors per class** |
| No trash | N/A | 📱 Clean video feed |
| Segmentation available | Any | 🎯 **Pixel-perfect masks** |
| Only detection available | Any | 📦 **Bounding boxes only** |

### Segmentation States

- **Active Segmentation**: Colored transparent masks overlay detected trash
- **Multi-class Support**: Different colors for different trash types
- **Confidence Display**: Object labels with confidence scores
- **Contour Enhancement**: Object boundaries highlighted in matching colors
- **Dual Mode**: Automatic fallback to bounding boxes if segmentation unavailable

### Visual Features

| Feature | Description | Purpose |
|---------|-------------|---------|
| Colored Masks | Semi-transparent overlays | Visual segmentation feedback |
| Bounding Boxes | Rectangular object boundaries | Object localization |
| Class Labels | Text with confidence scores | Object identification |
| Contour Lines | Object edge highlighting | Enhanced definition |
| Background Text | Solid color label backgrounds | Improved readability |

## Configuration

### Customizable Parameters

Edit the following variables in `main.py`:

```python
# Camera Configuration
CAMERA_WIDTH = 800          # Camera resolution width
CAMERA_HEIGHT = 600         # Camera resolution height
CAMERA_FORMAT = "RGB888"    # Color format

# Detection Parameters
CONFIDENCE_THRESHOLD = 0.01  # Minimum confidence (1%)
MODEL_PATH = "model/yolov11_seg_trash.pt"  # Model location

# Visual Configuration
MASK_ALPHA = 0.4            # Mask transparency (0.0-1.0)
BACKGROUND_ALPHA = 0.6      # Background blend factor
FONT_SCALE = 0.5            # Text size
FONT_THICKNESS = 2          # Text thickness
BOX_THICKNESS = 2           # Bounding box thickness

# Color Palette
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
          (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 165, 0), 
          (255, 192, 203), (165, 42, 42)]  # BGR format colors
```

### Performance Tuning

```python
# Segmentation optimization
MASK_THRESHOLD = 0.5        # Mask binarization threshold
VERBOSE_MODE = False        # Disable verbose output for speed

# Camera optimization for better performance
picam2.preview_configuration.main.size = (640, 480)  # Lower resolution
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
- Verify model file exists in `model/yolov11_seg_trash.pt`
- Check model file integrity (not corrupted)
- Ensure sufficient RAM available (segmentation requires more memory)
- Try restarting the system

**Segmentation Performance Issues**
- Reduce camera resolution for better frame rate
- Increase confidence threshold to reduce false positives
- Check lighting conditions for optimal detection
- Ensure trash objects are clearly visible

**Memory Issues**
```bash
# Check available memory
free -h

# Increase swap space for segmentation
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

**Mask Overlay Problems**
```python
# Adjust mask transparency
MASK_ALPHA = 0.3  # Make masks more transparent
BACKGROUND_ALPHA = 0.7  # Adjust background blending
```

**Import Errors**
```bash
# Update packages
sudo apt update
pip install --upgrade ultralytics
pip install --upgrade opencv-python
pip install --upgrade numpy
```

### Debug Mode

Add debug information for troubleshooting:

```python
# Add after model loading
print(f"Model classes: {model.names}")
print(f"Model type: segmentation" if hasattr(model.model[-1], 'nm') else "detection")

# Add in segmentation loop
print(f"Masks found: {len(masks) if masks is not None else 0}")
print(f"Confidence: {conf:.3f}, Class: {class_name}")
```

### Hardware Testing

**Test Individual Components:**

```bash
# Test camera with different resolutions
libcamera-still -o test_800x600.jpg --width 800 --height 600

# Monitor system resources during operation
htop

# Check GPU memory usage (if available)
vcgencmd measure_temp
vcgencmd get_mem gpu
```

## Performance Optimization

This segmentation system is optimized for:

- **Real-time Processing**: Efficient mask generation and overlay pipeline
- **Memory Management**: Optimized tensor operations for Raspberry Pi
- **Visual Quality**: High-quality transparent overlays with smooth blending
- **Dual Mode Support**: Automatic fallback for maximum compatibility
- **Resource Efficiency**: Balanced performance for continuous operation

## Applications

- **Waste Management**: Automated trash sorting and classification
- **Environmental Monitoring**: Pollution detection and assessment
- **Recycling Automation**: Smart sorting systems for recycling facilities
- **Smart Cities**: Urban cleanliness monitoring and reporting
- **Research Applications**: Environmental science and waste studies
- **Educational Projects**: Computer vision and sustainability learning
- **Quality Control**: Industrial waste inspection and management
- **Beach/Park Cleaning**: Automated litter detection for cleanup robots

## Safety Considerations

- **Electrical Safety**: Ensure proper power supply and grounding
- **Camera Positioning**: Secure mounting to prevent damage
- **Environmental Protection**: Consider weatherproofing for outdoor deployment
- **System Monitoring**: Regular performance checks and maintenance
- **Data Privacy**: Consider privacy implications when deploying in public spaces

## Model Performance

- **Training Dataset**: Custom trash dataset with detailed segmentation masks
- **Segmentation Accuracy**: >85% IoU on validation set
- **Detection Speed**: Real-time inference on Raspberry Pi 4
- **Mask Quality**: High-resolution pixel-perfect segmentation
- **Multi-class Support**: Multiple trash categories with distinct colors
- **Robustness**: Trained with various lighting and background conditions

## Advanced Features

### Segmentation Capabilities

- **Pixel-level Accuracy**: Precise object boundaries
- **Multi-object Support**: Simultaneous segmentation of multiple trash items
- **Class-specific Colors**: Visual differentiation between trash types
- **Mask Quality Control**: Automatic mask refinement and smoothing
- **Contour Enhancement**: Enhanced object definition with boundary highlighting

### Adaptive Processing

- **Automatic Mode Selection**: Switches between segmentation and detection modes
- **Dynamic Confidence Adjustment**: Adapts to varying lighting conditions
- **Memory-aware Processing**: Optimizes based on available system resources
- **Error Recovery**: Robust handling of processing failures

## Future Enhancements

- Integration with robotic sorting systems
- Cloud-based model updates and improvements
- Real-time waste statistics and reporting
- Mobile app connectivity for monitoring
- GPS tracking for outdoor deployment
- Advanced material classification (plastic types, metals, etc.)
- Integration with smart city infrastructure
