# Light Tracking Servo System
A Raspberry Pi-based light tracking system that uses LDR (Light Dependent Resistor) sensors to detect light sources and automatically moves a servo motor to follow the brightest direction.

## Features
- **Automatic light tracking** using dual LDR sensors
- **Servo motor control** with precise positioning
- **Real-time light detection** from left and right directions
- **Smart positioning logic** with center, left, and right positions
- **Graceful shutdown** with proper GPIO cleanup
- **Continuous monitoring** with adjustable response time

## Hardware Requirements

### Components
- Raspberry Pi (any model with GPIO pins)
- Servo Motor (standard 180-degree servo)
- 2x LDR (Light Dependent Resistor) sensors

- Breadboard and jumper wires
- External power supply for servo (5V recommended)

### Wiring Diagram
| Component | GPIO Pin | Physical Pin | Notes |
|-----------|----------|--------------|-------|
| Servo Signal | GPIO 27 | Pin 13 | PWM control signal |
| Left LDR | GPIO 17 | Pin 11 | Left light sensor |
| Right LDR | GPIO 22 | Pin 15 | Right light sensor |
| Servo Power | 5V | Pin 2 or 4 | External supply recommended |
| Ground | GND | Pin 6, 9, 14, 20 | Common ground |

### LDR Circuit Setup
LDR sensors are connected directly to GPIO pins:
- LDR connected between GPIO pin and GND
- When light hits LDR: GPIO reads LOW (0)
- When no light: GPIO reads HIGH (1)

## Software Requirements

### System Requirements
- Python 3.7+
- Raspberry Pi OS
- GPIO access permissions
- lgpio library

## Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd light-tracking-servo
   ```

2. **Install required Python packages**
   ```bash
   pip install lgpio
   ```

3. **Enable GPIO permissions** (if needed)
   ```bash
   sudo usermod -a -G gpio $USER
   ```

4. **Connect hardware** according to the wiring diagram

## Usage

### Running the System
```bash
python light_tracker.py
```

### Stopping the System
Press `Ctrl+C` to gracefully shutdown the light tracking system.

## System Behavior

### Servo Positions
| Light Condition | Servo Position | Angle | Description |
|-----------------|----------------|-------|-------------|
| Both sides | Center | 90° | Light detected on both LDRs |
| Left only | Left | 45° | Light detected only on left LDR |
| Right only | Right | 135° | Light detected only on right LDR |
| No light | Center | 90° | No light detected on either side |

### Control Logic
- **Sensor Reading**: LDR outputs LOW (0) when light is detected
- **Response Time**: 1 second delay between position updates
- **Positioning**: 45-degree increments for smooth movement
- **Default State**: Center position when no directional preference

### PWM Signal Details
- **Pulse Width Range**: 1ms to 2ms
- **0 degrees**: 1ms pulse width
- **90 degrees**: 1.5ms pulse width
- **180 degrees**: 2ms pulse width
- **Signal Frequency**: Manual PWM implementation

## Configuration

### Customizable Parameters
Edit the following variables in the code:

```python
# GPIO pin assignments
SERVO_PIN = 27      # Servo control pin
LDR_PIN_LEFT = 17   # Left LDR sensor pin
LDR_PIN_RIGHT = 22  # Right LDR sensor pin

# Servo positions (degrees)
CENTER_POSITION = 90    # Straight ahead
LEFT_POSITION = 45      # Left turn
RIGHT_POSITION = 135    # Right turn

# Timing parameters
RESPONSE_DELAY = 1      # Seconds between readings
```

### Advanced Servo Control
```python
def move_servo(angle):
    pulse_width = 1 + (angle / 180.0)  # Convert angle to pulse width
    set_servo_pulsewidth(h, SERVO_PIN, pulse_width)
```

## Troubleshooting

### Common Issues

**Servo Not Moving**
- Check power supply (servo may need external 5V)
- Verify PWM signal connections
- Test servo with multimeter
- Ensure proper ground connections

**LDR Sensors Not Responding**
- Check LDR orientation and lighting conditions
- Test sensor readings with debug prints
- Ensure proper circuit connections

**Permission Denied (GPIO)**
```bash
sudo usermod -a -G gpio $USER
# Then log out and back in
```

**Module Import Errors**
```bash
pip install --upgrade lgpio
```

**Servo Jittering**
- Add capacitor to power line (100-1000µF)
- Use external power supply
- Check for loose connections
- Reduce response frequency

### Debug Mode
Add debug prints to monitor sensor readings:
```python
print(f"Debug: Left LDR={light_left}, Right LDR={light_right}, Angle={current_angle}")
```

### Calibration Tips
- Test LDR sensitivity in different lighting conditions
- Adjust servo positions for optimal tracking range
- Fine-tune response delay for smooth operation
- Consider adding hysteresis to prevent oscillation

### Servo Connection
- Red wire: 5V power
- Brown/Black wire: Ground
- Orange/Yellow wire: GPIO signal pin

## Safety Considerations
- Ensure servo power supply can handle current requirements
- Protect GPIO pins from voltage spikes
- Implement proper error handling for hardware failures
