import time
import board
import adafruit_dht
import lgpio

# LED pin definitions
LED_NORMAL = 17     # Green LED - normal operation status
LED_ALERT = 27      # Yellow LED - temperature rise alert
LED_WARNING = 22    # Red LED - consecutive temperature rise warning

# DHT11 temperature and humidity sensor on GPIO 4 (board.D4)
dht = adafruit_dht.DHT11(board.D4)

# Initialize GPIO for LEDs
h = lgpio.gpiochip_open(0)  # Open GPIO chip 0
for pin in [LED_NORMAL, LED_ALERT, LED_WARNING]:
    lgpio.gpio_claim_output(h, pin)  # Set pins as outputs

def led_on(pin):
    """Turn on LED connected to specified pin"""
    lgpio.gpio_write(h, pin, 1)

def led_off(pin):
    """Turn off LED connected to specified pin"""
    lgpio.gpio_write(h, pin, 0)

try:
    # Startup sequence: Turn on NORMAL LED for 1s, then blink twice and stay on
    led_on(LED_NORMAL)
    time.sleep(1)
    
    # Blink sequence (2 times) to indicate system initialization
    for _ in range(2):
        led_off(LED_NORMAL)
        time.sleep(0.3)
        led_on(LED_NORMAL)
        time.sleep(0.3)
    
    # Initialize variables for temperature monitoring
    temps = []                      # List to store last 5 temperature readings
    consecutive_alerts = 0          # Counter for consecutive temperature rise alerts
    
    # Main monitoring loop
    while True:
        try:
            # Read temperature and humidity from DHT11 sensor
            temperature = dht.temperature
            humidity = dht.humidity
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
        except RuntimeError as e:
            # Handle sensor reading errors (common with DHT sensors)
            print("Error reading from sensor:", e.args[0])
            temperature = None
        
        if temperature is not None:
            # Add current temperature to the list
            temps.append(temperature)
            
            # Keep only the last 5 measurements (25 seconds of data at 5s intervals)
            if len(temps) > 5:
                temps.pop(0)  # Remove oldest measurement
            
            # Check for temperature rise pattern (need 5 measurements)
            if len(temps) == 5:
                # Calculate temperature delta between newest and oldest reading
                delta = temps[-1] - temps[0]  # Current temp - temp from 20s ago
                
                if delta > 1:  # Temperature rose more than 1°C in 20 seconds
                    consecutive_alerts += 1
                    
                    # Turn on ALERT LED and turn off NORMAL LED
                    led_on(LED_ALERT)
                    led_off(LED_NORMAL)
                    
                    # If 2 consecutive alerts, turn on WARNING LED and turn off ALERT LED
                    if consecutive_alerts >= 2:
                        led_on(LED_WARNING)   # Critical warning - consecutive temperature rises
                        led_off(LED_ALERT)    # Turn off yellow LED when red is active
                    else:
                        led_off(LED_WARNING)
                        
                else:  # Temperature stable or decreasing
                    consecutive_alerts = 0  # Reset consecutive alert counter
                    
                    # Normal operation: only NORMAL LED on
                    led_on(LED_NORMAL)
                    led_off(LED_ALERT)
                    led_off(LED_WARNING)
                    
            else:
                # Not enough measurements yet - show normal status
                led_on(LED_NORMAL)
                led_off(LED_ALERT)
                led_off(LED_WARNING)
                
        else:
            # Sensor reading error - keep NORMAL LED on to indicate standby mode
            led_on(LED_NORMAL)
            led_off(LED_ALERT)
            led_off(LED_WARNING)
        
        # Wait 5 seconds before next reading
        time.sleep(5)
        
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Exiting and turning off LEDs...")
    
finally:
    # Cleanup: turn off all LEDs and close GPIO
    for pin in [LED_NORMAL, LED_ALERT, LED_WARNING]:
        led_off(pin)
    lgpio.gpiochip_close(h)  # Close GPIO chip connection
