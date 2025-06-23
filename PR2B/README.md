# Motion Detection System with Smart Lighting

A Raspberry Pi-based motion detection system that automatically controls LED strip lighting based on movement detection and ambient light conditions. The system uses an ultrasonic sensor to detect nearby movement and only activates lighting when it's dark, providing an energy-efficient automated lighting solution.

## Features

- **Intelligent motion detection** using HC-SR04 ultrasonic sensor
- **Ambient light sensing** with LDR sensor for energy optimization
- **Smart LED strip control** with NeoPixel RGB lighting
- **Energy-saving operation** - lights only activate in dark conditions
- **Configurable parameters** for sensitivity and timing customization
- **Automatic timeout control** with adjustable light duration
- **Robust error handling** and sensor fault recovery
- **Graceful shutdown** with proper GPIO cleanup

## Hardware Requirements

### Components

- Raspberry Pi (any model with GPIO pins and SPI support)
- HC-SR04 Ultrasonic Distance Sensor
- 1x LDR (Light Dependent Resistor) sensor
- NeoPixel LED Strip (WS2812B compatible)
- Breadboard and jumper wires
- External power supply for LED strip (if using many LEDs)

### Wiring Diagram

| Component | GPIO Pin | Physical Pin | Notes |
|-----------|----------|--------------|-------|
| HC-SR04 Trigger | GPIO 17 | Pin 11 | Ultrasonic sensor trigger |
| HC-SR04 Echo | GPIO 27 | Pin 13 | Ultrasonic sensor echo |
| LDR Sensor | GPIO 22 | Pin 15 | Light sensor (digital input) |
| NeoPixel Data | GPIO 10 (MOSI) | Pin 19 | LED strip data line |
| Ground | GND | Pin 6, 9, 14, 20 | Common ground |
| Power | 5V | Pin 2, 4 | Sensor and LED power |

## Software Requirements

### System Requirements

- Python 3.7+
- Raspberry Pi OS with SPI enabled
- GPIO access permissions

### Dependencies

- `lgpio`
- `board`
- `neopixel_spi`
- `time`

## Installation

1. **Enable SPI interface**
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > SPI > Enable
   ```

2. **Clone or download the project files**
   ```bash
   git clone https://github.com/EVTA-EU/AISVE.git
   cd AISVE/PR2B
   ```

3. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Enable GPIO permissions** (if needed)
   ```bash
   sudo usermod -a -G gpio $USER
   ```

5. **Connect hardware** according to the wiring diagram

## Usage

### Running the System

```bash
python main.py
```

### System Operation

The system operates automatically once started:

1. **Continuous Monitoring**: Ultrasonic sensor measures distance every 100ms
2. **Motion Detection**: Detects objects within the configured threshold distance
3. **Light Assessment**: LDR sensor checks ambient light conditions
4. **Smart Activation**: LED strip turns on only when motion is detected AND it's dark
5. **Automatic Timeout**: Lights turn off after the configured duration

### Stopping the System

Press `Ctrl+C` to gracefully shutdown the motion detection system.

## System Behavior

### Detection Logic

| Condition | Motion Detected | Light Level | LED Action |
|-----------|----------------|-------------|------------|
| Object < 50cm | ✅ Yes | 🌙 Dark | 💡 **Lights ON** |
| Object < 50cm | ✅ Yes | ☀️ Bright | 💡 Lights OFF |
| Object > 50cm | ❌ No | 🌙 Dark | 💡 Lights OFF |
| Object > 50cm | ❌ No | ☀️ Bright | 💡 Lights OFF |

### Light States

- **Lights ON**: All 12 LEDs illuminate in white when motion detected in dark conditions
- **Timer Active**: Lights remain on for 5 seconds after initial detection
- **Automatic OFF**: Lights turn off when timer expires, regardless of continued presence
- **Re-activation**: System immediately responds to new motion detection

### Status Indicators

| Console Output | Meaning | Description |
|----------------|---------|-------------|
| `Distance: XX.Xcm` | Sensor Reading | Current ultrasonic distance measurement |
| `Object detected: True/False` | Detection Status | Whether object is within threshold |
| `Dark: True/False` | Light Condition | Ambient light level assessment |
| `Motion detected in dark environment - Lights ON` | Activation | LED strip has been activated |
| `Lights OFF` | Deactivation | LED strip has been deactivated |

## Configuration

### Customizable Parameters

Edit the following variables in `main.py`:

```python
# GPIO Pin Configuration
TRIGGER_PIN = 17            # Ultrasonic sensor trigger
ECHO_PIN = 27              # Ultrasonic sensor echo
LDR_PIN = 22               # Light sensor pin

# Detection Parameters
MOTION_THRESHOLD = 50.0     # Detection distance (cm)
LIGHT_ON_DURATION = 5.0     # Light duration (seconds)
MEASUREMENT_INTERVAL = 0.1  # Sensor update rate (seconds)

# LED Configuration
NUM_PIXELS = 12            # Number of LEDs
LED_COLOR = 0xFFFFFF       # LED color (white)
LED_BRIGHTNESS = 0.5       # Brightness level (0.0-1.0)
```

### Sensitivity Adjustments

```python
# Motion sensitivity (distance change threshold)
DISTANCE_CHANGE_THRESHOLD = 5.0  # cm

# Timeout settings
SENSOR_TIMEOUT = 0.1            # seconds
```

## Troubleshooting

### Common Issues

**Ultrasonic Sensor Not Working**
- Check wiring connections for trigger and echo pins
- Verify 5V power supply to sensor
- Ensure proper ground connections
- Test with multimeter for voltage levels

**LED Strip Not Lighting**
```bash
# Check SPI is enabled
ls /dev/spi*
# Should show /dev/spidev0.0 and /dev/spidev0.1
```

**LDR Sensor Always Dark/Bright**
- Check LDR wiring connections
- Test sensor response with different lighting
- Adjust sensor logic if needed (invert reading)

**Permission Denied (GPIO)**
```bash
sudo usermod -a -G gpio $USER
# Then log out and back in
```

**Distance Measurement Timeouts**
- Increase `SENSOR_TIMEOUT` value
- Check for electrical interference
- Ensure clear path for ultrasonic waves

**LED Strip Drawing Too Much Current**
- Use external power supply for LED strip
- Reduce `LED_BRIGHTNESS` value
- Limit number of simultaneous LEDs

### Debug Mode

Add debug information by modifying the code:

```python
def measure_distance():
    distance = # ... measurement code
    print(f"Debug: Raw distance = {distance}cm")
    return distance
```

### Hardware Testing

**Test Individual Components:**

```bash
# Test SPI devices
ls /dev/spi*

# Test GPIO functionality
# Use a simple LED test script first
```

## Energy Efficiency Benefits

This motion detection system promotes:

- **Smart Energy Usage**: Lights only activate when needed
- **Automated Control**: No manual switches required
- **Ambient Light Awareness**: Prevents unnecessary daytime activation
- **Customizable Timing**: Adjustable light duration for optimal efficiency
- **LED Technology**: Energy-efficient NeoPixel LEDs with brightness control

## Safety Considerations

- **Electrical Safety**: Ensure proper grounding and insulation
- **Component Ratings**: Verify all components are rated for operating conditions


## Applications

- **Hallway Lighting**: Automatic corridor illumination
- **Stairway Safety**: Motion-activated step lighting
- **Closet Lighting**: Hands-free wardrobe illumination
- **Garage Entry**: Automatic lighting for dark entrances
- **Security Enhancement**: Perimeter motion lighting
- **Energy Conservation**: Smart lighting in commercial spaces
