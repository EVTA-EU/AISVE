# Smart Waste Classification System

An intelligent Raspberry Pi-based IoT system that automatically detects objects, activates LED lighting in low-light conditions, and classifies waste types using YOLOv11 computer vision. The system features motion detection, environmental sensing, and real-time classification with visual feedback through an OLED display.

## Features

- **Intelligent Motion Detection** using ultrasonic sensors
- **Automatic LED Lighting** triggered by darkness and motion
- **Real-time Waste Classification** using YOLOv11 neural network
- **Environmental Light Sensing** with LDR sensor
- **OLED Display Interface** showing classification results and system status
- **Resource-Efficient Operation** with smart camera management
- **Multi-category Waste Classification** (Plastic, Paper, Cardboard, Glass, Organic)
- **Confidence Scoring** for reliable classification results
- **Graceful System Management** with automatic resource cleanup

## Hardware Requirements

### Core Components

- **Raspberry Pi 5**
- **Pi Camera Module** (v2 or v3 recommended)
- **HC-SR04 Ultrasonic Sensor** for distance measurement
- **LDR (Light Dependent Resistor)** for ambient light detection
- **SSD1306 OLED Display** (128x64, I2C interface)
- **WS2812B LED Strip** (12 pixels, NeoPixel compatible)
- **MicroSD Card** (32GB+ recommended)
- **Breadboard and Jumper Wires**


### Pin Configuration

| Component | Raspberry Pi Pin | GPIO Pin | Notes |
|-----------|------------------|----------|-------|
| Ultrasonic Trigger | Physical 11 | GPIO 17 | Output |
| Ultrasonic Echo | Physical 13 | GPIO 27 | Input |
| LDR Sensor | Physical 15 | GPIO 22 | Input (with pull-up) |
| OLED Display | SDA/SCL | GPIO 2/3 | I2C interface |
| LED Strip | SPI | SPI0 | NeoPixel SPI |

### Wiring Diagram

```
Raspberry Pi 4
├── GPIO 17 (Pin 11) ──── HC-SR04 Trigger
├── GPIO 27 (Pin 13) ──── HC-SR04 Echo
├── GPIO 22 (Pin 15) ──── LDR ──── 10kΩ ──── 3.3V
├── GPIO 2 (SDA) ─────── OLED SDA
├── GPIO 3 (SCL) ─────── OLED SCL
└── SPI0 ───────────── LED Strip Data
```

## Software Requirements

### System Requirements

- **Raspberry Pi OS** (latest version recommended)
- **Python 3.8+**
- **Camera interface enabled**
- **I2C interface enabled**
- **SPI interface enabled**
- **Minimum 4GB RAM** for YOLOv11 processing

### Dependencies

```python
# Core libraries
import cv2
import time
import board
import lgpio
import numpy as np

# Hardware interfaces
import neopixel_spi as neopixel
import adafruit_ssd1306
from picamera2 import Picamera2

# AI and image processing
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont

# System utilities
import threading
```

## Installation

### 1. System Setup

1. **Enable Camera Interface**
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > Camera > Enable
   ```

2. **Clone or download the project files**
   ```bash
   git clone https://github.com/EVTA-EU/AISVE.git
   cd AISVE/PR4
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

## Configuration

### System Parameters

Edit the configuration variables at the top of the main script:

```python
# ==================== DETECTION CONFIGURATION ====================
MOTION_THRESHOLD = 50.0      # Distance threshold for motion detection (cm)
LIGHT_ON_DURATION = 10.0     # How long LEDs stay on (seconds)
MEASUREMENT_INTERVAL = 0.2   # Sensor reading frequency (seconds)
CAMERA_TIMEOUT = 15.0        # Camera active duration after motion (seconds)

# ==================== LED STRIP CONFIGURATION ====================
NUM_PIXELS = 12              # Number of LEDs in strip
LED_COLOR = 0xFFFFFF         # LED color (white)
LED_BRIGHTNESS = 0.5         # LED brightness (0.0-1.0)

# ==================== CLASSIFICATION CONFIGURATION ====================
WASTE_CATEGORIES = {
    'plastic': 'PLASTIC',
    'paper': 'PAPER', 
    'cardboard': 'CARDBOARD',
    'green-glass': 'GLASS',
    'trash': 'TRASH'
}
```



## Usage

### Running the System

```bash
# Activate virtual environment
source waste_classifier/bin/activate

# Run the main program
python3 main.py
```

### System Operation Flow

1. **Startup**: System initializes hardware components and displays startup message
2. **Monitoring**: Continuous distance monitoring for motion detection
3. **Motion Detection**: When object detected within threshold distance:
   - Camera activates for classification
   - LEDs turn on if environment is dark
4. **Classification**: YOLOv11 processes camera feed and identifies waste type
5. **Display Update**: OLED shows classification results and system status
6. **Resource Management**: Camera deactivates after timeout to save resources

### System States

| State | Description | Display | LED Status |
|-------|-------------|---------|------------|
| **Waiting** | No motion detected | "WAITING..." | Off |
| **Active** | Object detected, camera on | Classification result | On (if dark) |
| **Classifying** | Processing camera feed | "Type: [CATEGORY]" | Variable |
| **Idle** | Post-detection cooldown | Last classification | Automatic |

### User Interface

**OLED Display Layout:**
```
┌─────────────────────────┐
│      CLASSIFIER         │
│                         │
│ Type: PLASTIC           │
│ Conf: 87.3%             │
│                         │
│ CAM: ACTIVE  LED: ON    │
└─────────────────────────┘
```

**Status Indicators:**
- **CAM Status**: ACTIVE/IDLE
- **LED Status**: ON/OFF
- **Classification**: Type and confidence percentage

## Model Training

The system uses a custom-trained YOLOv11 model for waste classification. Training involves:

### Training Process

1. **Dataset Preparation**: Collect diverse waste images across all categories
2. **Data Annotation**: Label objects with bounding boxes and categories
3. **Model Configuration**: Set up YOLOv11 for multi-class classification
4. **Training**: Use transfer learning from pre-trained YOLOv11 weights
5. **Validation**: Test model accuracy across different waste types
6. **Export**: Save model in PyTorch format (.pt)

### Recommended Training Environment

- **Google Colab with GPU** (strongly recommended)
- **Minimum 6GB GPU memory**

### Training Tips

```python
# Example training configuration
from ultralytics import YOLO

model = YOLO('yolov11n.pt')  # Start with nano model for speed
results = model.train(
    data='waste_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='gpu'
)
```

## Troubleshooting

### Common Issues

**Hardware Problems**

```bash
# Camera not detected
vcgencmd get_camera
# Should return: supported=1 detected=1

# I2C device not found
sudo i2cdetect -y 1
# OLED should appear at 0x3C

# GPIO permission errors
sudo usermod -a -G gpio $USER
# Then logout and login again
```

**Software Issues**

```bash
# Import errors
pip install --upgrade ultralytics opencv-python

# Memory issues - increase swap
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

**Performance Issues**

```python
# Reduce camera resolution for better performance
self.picam2.preview_configuration.main.size = (640, 480)

# Increase measurement interval
MEASUREMENT_INTERVAL = 0.5  # Slower but less CPU intensive

# Adjust confidence threshold
if confidence > 50:  # Lower threshold for more detections
```

### Debug Mode

Enable detailed logging by adding debug prints:

```python
# Add to main loop
print(f"Distance: {distance:.1f}cm | Dark: {dark_environment}")
print(f"Classification: {best_label} ({highest_conf:.1f}%)")
print(f"Camera active: {current_time < self.camera_active_until}")
```

### Hardware Testing

**Test Components Individually:**

```python
# Test ultrasonic sensor
def test_ultrasonic():
    # Add distance measurement code
    print(f"Distance: {distance:.1f}cm")

# Test OLED display
def test_oled():
    oled.fill(0)
    oled.text("TEST", 0, 0, 1)
    oled.show()

# Test LED strip
def test_leds():
    for i in range(NUM_PIXELS):
        pixels[i] = (255, 0, 0)  # Red
    pixels.show()
```

## Performance Optimization

### System Optimization

- **Smart Camera Management**: Camera only active when needed
- **Efficient Sensor Polling**: Optimized measurement intervals
- **Resource Cleanup**: Proper GPIO and camera resource management
- **Memory Management**: Garbage collection and resource monitoring

### Detection Optimization

```python
# Optimize YOLOv11 inference
model = YOLO("model/yolov11_garbage.pt")
model.fuse()  # Fuse model layers for speed

# Reduce image processing overhead
frame = cv2.resize(frame, (416, 416))  # Smaller input size
```

## Applications

### Primary Use Cases

- **Smart Recycling Bins**: Automated waste sorting systems
- **Environmental Monitoring**: Waste detection in public spaces
- **Educational Projects**: STEM learning and environmental awareness
- **Home Automation**: Smart waste management systems
- **Research Applications**: Waste classification studies

### Integration Possibilities

- **IoT Platforms**: MQTT integration for remote monitoring
- **Mobile Apps**: Real-time status and statistics
- **Cloud Services**: Data logging and analytics
- **Smart Home Systems**: Integration with home automation
- **Robotic Systems**: Interface with sorting robots

## Safety and Maintenance

### Safety Considerations

- **Electrical Safety**: Proper grounding and power supply protection
- **Camera Privacy**: Consider privacy implications in deployment
- **LED Brightness**: Adjust brightness to prevent eye strain
- **Secure Mounting**: Ensure stable hardware mounting

## Advanced Features

### Future Enhancements

- **Multi-angle Classification**: Multiple camera support
- **Size Estimation**: Object size measurement
- **Material Analysis**: Advanced material identification
- **Cloud Integration**: Remote monitoring and updates
- **Voice Feedback**: Audio classification announcements
- **Mobile Interface**: Smartphone app integration

### Customization Options

```python
# Custom classification categories
CUSTOM_CATEGORIES = {
    'electronics': 'E-WASTE',
    'batteries': 'HAZARDOUS',
    'textiles': 'FABRIC'
}

# Custom LED patterns
def custom_led_pattern():
    # Implement rainbow or breathing effects
    pass

# Custom display layouts
def custom_oled_display():
    # Add graphics, icons, or animations
    pass
```


