# Temperature Monitoring System with LED Indicators

A Raspberry Pi-based temperature monitoring system that uses a DHT11 sensor and LED indicators to provide real-time temperature alerts and warnings.

## Features

- **Real-time temperature and humidity monitoring** using DHT11 sensor
- **Visual LED status indicators** for different system states
- **Temperature rise detection** with configurable thresholds
- **Escalating alert system** for consecutive temperature increases
- **Robust error handling** and sensor fault recovery
- **Graceful shutdown** with proper GPIO cleanup

## Hardware Requirements

### Components
- Raspberry Pi (any model with GPIO pins)
- DHT11 Temperature and Humidity Sensor
- 3x LEDs (Green, Yellow, Red recommended)
- 3x 220Ω resistors (for LED current limiting)
- Breadboard and jumper wires

### Wiring Diagram

| Component | GPIO Pin | Physical Pin | Notes |
|-----------|----------|--------------|-------|
| DHT11 Data | GPIO 4 | Pin 7 | Temperature sensor |
| Green LED | GPIO 17 | Pin 11 | Normal operation |
| Yellow LED | GPIO 27 | Pin 13 | Temperature alert |
| Red LED | GPIO 22 | Pin 15 | Critical warning |
| Ground | GND | Pin 6, 9, 14, 20 | Common ground |
| Power | 3.3V to 5V | Pin 1, 17 | DHT11 power |

## Software Requirements

### System Requirements
- Python 3.7+
- Raspberry Pi OS
- GPIO access permissions

## Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd temperature-monitoring-system
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Enable GPIO permissions** (if needed)
   ```bash
   sudo usermod -a -G gpio $USER
   ```

4. **Connect hardware** according to the wiring diagram

## Usage

### Running the System
```bash
python main.py
```

### Stopping the System
Press `Ctrl+C` to gracefully shutdown the monitoring system.

## System Behavior

### LED Status Indicators

| LED State | Meaning | Description |
|-----------|---------|-------------|
| 🟢 Green | Normal Operation | Temperature stable, system running normally |
| 🟡 Yellow | Temperature Alert | Temperature increased >1°C in 20 seconds |
| 🔴 Red | Critical Warning | Two consecutive temperature rise alerts |
| 🟢 Green (Error) | Sensor Error | DHT11 reading failed, system in standby |

### Startup Sequence
1. Green LED turns on for 1 second
2. Green LED blinks twice (0.3s intervals)
3. Green LED remains on - system ready

### Alert Logic
- **Monitoring Window**: 25 seconds (5 readings at 5-second intervals)
- **Alert Threshold**: Temperature increase >1°C over 20 seconds
- **Warning Trigger**: 2 consecutive alerts
- **Reset Condition**: Temperature stabilizes (≤1°C increase)

## Configuration

### Customizable Parameters

Edit the following variables in `temperature_monitor.py`:

```python
# LED GPIO pins
LED_NORMAL = 17     # Green LED pin
LED_ALERT = 27      # Yellow LED pin  
LED_WARNING = 22    # Red LED pin

# Sensor configuration
dht = adafruit_dht.DHT11(board.D4)  # DHT11 on GPIO 4

# Monitoring parameters
TEMP_THRESHOLD = 1      # Temperature rise threshold (°C)
READING_INTERVAL = 5    # Seconds between readings
HISTORY_SIZE = 5        # Number of readings to keep
ALERT_THRESHOLD = 2     # Consecutive alerts for warning
```

## Troubleshooting

### Common Issues

**DHT11 Sensor Errors**
- DHT sensors occasionally fail to read - this is normal
- System continues monitoring and shows standby status
- Check wiring if errors persist

**Permission Denied (GPIO)**
```bash
sudo usermod -a -G gpio $USER
# Then log out and back in
```

**Module Import Errors**
```bash
pip install --upgrade adafruit-circuitpython-dht lgpio
```

**LEDs Not Working**
- Check resistor values (220Ω recommended)
- Verify GPIO pin connections
- Test LEDs with multimeter

### Debug Mode
Add debug prints by modifying the code:
```python
print(f"Debug: temp_delta={delta}, alerts={alertas_consecutivos}")
```
