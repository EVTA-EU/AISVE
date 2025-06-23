# Environmental Monitoring Station

A Raspberry Pi-based environmental monitoring system that displays real-time temperature, humidity, and ambient light data on an OLED screen with interactive button navigation.

## Features

- **Multi-parameter environmental monitoring** using DHT11 and LDR sensors
- **Interactive OLED display** with button-controlled navigation
- **Real-time environmental awareness** with comfort level assessments
- **Energy-saving recommendations** based on lighting conditions
- **Thermal comfort analysis** with temperature categorization
- **Humidity level evaluation** for optimal indoor conditions
- **Robust error handling** and sensor fault recovery
- **Graceful shutdown** with proper GPIO cleanup

## Hardware Requirements

### Components

- Raspberry Pi (any model with GPIO pins and I2C support)
- DHT11 Temperature and Humidity Sensor
- 1x LDR (Light Dependent Resistor) sensor
- SSD1306 OLED Display (128x64, I2C)
- 1x Push button (momentary switch)
- 1x 10kΩ resistor (for button pull-up, if needed)
- Breadboard and jumper wires

### Wiring Diagram

| Component | GPIO Pin | Physical Pin | Notes |
|-----------|----------|--------------|-------|
| DHT11 Data | GPIO 4 | Pin 7 | Temperature & humidity sensor |
| LDR Sensor | GPIO 17 | Pin 11 | Light sensor (digital input) |
| Mode Button | GPIO 23 | Pin 16 | Cycle display modes button |
| OLED SDA | GPIO 2 (SDA) | Pin 3 | I2C data line |
| OLED SCL | GPIO 3 (SCL) | Pin 5 | I2C clock line |
| Ground | GND | Pin 6, 9, 14, 20 | Common ground |
| Power | 3.3V/5V | Pin 1, 17 | Sensor and display power |

## Software Requirements

### System Requirements

- Python 3.7+
- Raspberry Pi OS with I2C enabled
- GPIO access permissions

### Dependencies

- `adafruit-circuitpython-dht`
- `adafruit-circuitpython-ssd1306`
- `lgpio`
- `Pillow (PIL)`
- `board`

## Installation

1. **Enable I2C interface**
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > I2C > Enable
   ```

2. **Clone or download the project files**
   ```bash
   git clone https://github.com/EVTA-EU/AISVE.git
   cd AISVE/PR2A
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

### Button Control

- **Single Button (GPIO 23)**: Press to cycle through display modes
  - **Sequence**: All Data → Temperature → Humidity → Light → All Data (repeats)

### Stopping the System

Press `Ctrl+C` to gracefully shutdown the monitoring system.

## System Behavior

### Display Modes

| Mode | Display Content | Information Shown |
|------|----------------|-------------------|
| **All Data** | Overview screen | Temperature, humidity, light level summary |
| **Temperature** | Detailed temp view | Temperature value + comfort assessment |
| **Humidity** | Detailed humidity view | Humidity percentage + level evaluation |
| **Light** | Detailed light view | Light detection + energy recommendations |

### Environmental Assessments

#### Temperature Comfort Levels
- **Cold**: < 18°C
- **Comfortable**: 18°C - 26°C  
- **Hot**: > 26°C

#### Humidity Levels
- **Dry**: < 30%
- **Optimal**: 30% - 70%
- **Humid**: > 70%

#### Light Detection States
- **Bright**: Light detected on LDR sensor
- **Dark**: No light detected on sensor

### Status Indicators

| Indicator | Meaning | Description |
|-----------|---------|-------------|
| 📺 OLED Display | System Status | Shows environmental data and system state |
| 🔘 Button Response | Mode Selection | Visual feedback on display mode changes |

## Configuration

### Customizable Parameters

Edit the following variables in `environmental_station.py`:

```python
# GPIO Pin Configuration
DHT_PIN = board.D4          # DHT11 sensor pin
LDR_PIN = 17               # Light sensor
BUTTON_MODE = 23           # Mode cycling button

# Display Configuration
WIDTH = 128                 # OLED display width
HEIGHT = 64                 # OLED display height

# System Parameters
BUTTON_DEBOUNCE = 0.3       # Button debounce time (seconds)
UPDATE_INTERVAL = 0.5       # Display update interval (seconds)
```

### Comfort Level Thresholds

```python
# Temperature comfort ranges (°C)
TEMP_COLD_THRESHOLD = 18
TEMP_HOT_THRESHOLD = 26

# Humidity level ranges (%)
HUMIDITY_DRY_THRESHOLD = 30
HUMIDITY_HUMID_THRESHOLD = 70
```

## Troubleshooting

### Common Issues

**DHT11 Sensor Errors**
- DHT sensors occasionally fail to read - this is normal
- System displays "Sensor Error" and continues monitoring
- Check wiring and power connections if errors persist

**OLED Display Not Working**
```bash
# Check I2C devices
sudo i2cdetect -y 1
# Should show device at address 0x3C
```

**Button Not Responding**
- Check button wiring and pull-up resistors
- Verify GPIO pin assignments
- Test with multimeter for proper voltage levels

**Permission Denied (GPIO)**
```bash
sudo usermod -a -G gpio $USER
# Then log out and back in
```

**Module Import Errors**
```bash
pip install --upgrade adafruit-circuitpython-dht adafruit-circuitpython-ssd1306 lgpio Pillow
```

**Light Sensors Always Dark/Bright**
- Check LDR wiring and voltage divider resistors
- Verify sensor sensitivity in different lighting conditions
- Adjust threshold logic if needed

### Debug Mode

Add debug information by modifying the code:

```python
def read_sensors(self):
    print(f"Debug: Temperature={self.temperature}°C, Humidity={self.humidity}%")
    print(f"Debug: Light Level={self.light_level}")
```

### Hardware Testing

**Test Individual Components:**

```bash
# Test I2C devices
sudo i2cdetect -y 1

# Test GPIO pins
gpio readall  # if wiringpi installed
```

## Environmental Benefits

This monitoring station promotes:

- **Energy Efficiency**: Light level monitoring for optimal lighting usage
- **Thermal Comfort**: Real-time temperature assessment for HVAC optimization  
- **Health Awareness**: Humidity monitoring for respiratory comfort
- **Environmental Consciousness**: Understanding of indoor climate conditions

## Future Enhancements

- Data logging to file or database
- Wireless connectivity for remote monitoring
- Mobile app integration
- Additional sensors (CO2, air quality)
- Automated alerts and notifications
- Historical data visualization



