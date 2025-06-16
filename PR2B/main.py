import time
import board
import lgpio
import neopixel_spi as neopixel

# GPIO pin definitions
TRIGGER_PIN = 17    # GPIO pin for ultrasonic sensor trigger
ECHO_PIN = 27       # GPIO pin for ultrasonic sensor echo
LDR_PIN = 22        # GPIO pin for LDR (Light Dependent Resistor) sensor

# NeoPixel LED strip configuration
NUM_PIXELS = 12                     # Number of LEDs in the strip
PIXEL_ORDER = neopixel.GRB         # Color order (Green, Red, Blue)
LED_COLOR = 0xFFFFFF               # White color for motion detection
LED_BRIGHTNESS = 0.5               # LED brightness (0.0 to 1.0)

# Motion detection parameters
MOTION_THRESHOLD = 50.0            # Distance threshold in cm to detect motion
LIGHT_ON_DURATION = 5.0            # How long to keep lights on after motion (seconds)
MEASUREMENT_INTERVAL = 0.1         # Time between distance measurements (seconds)

# Initialize GPIO chip
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, TRIGGER_PIN)    # Set trigger pin as output
lgpio.gpio_claim_input(h, ECHO_PIN)        # Set echo pin as input
lgpio.gpio_claim_input(h, LDR_PIN)         # Set LDR pin as input

# Initialize NeoPixel LED strip
spi = board.SPI()
pixels = neopixel.NeoPixel_SPI(
    spi, 
    NUM_PIXELS, 
    brightness=LED_BRIGHTNESS,
    pixel_order=PIXEL_ORDER,
    auto_write=False
)

# Global variables for motion tracking
previous_distance = None
lights_on_until = 0  # Timestamp when lights should turn off

def measure_distance():
    """
    Measure distance using the ultrasonic sensor.
    
    Returns:
        float: Distance in centimeters, or None if measurement fails
    """
    try:
        # Send 10-microsecond pulse to trigger pin
        lgpio.gpio_write(h, TRIGGER_PIN, 1)
        time.sleep(0.00001)  # 10 microseconds
        lgpio.gpio_write(h, TRIGGER_PIN, 0)
        
        # Wait for echo to start (pin goes HIGH)
        start_time = time.time()
        timeout = start_time + 0.1  # 100ms timeout
        
        while lgpio.gpio_read(h, ECHO_PIN) == 0:
            start_time = time.time()
            if start_time > timeout:
                return None  # Timeout occurred
        
        # Wait for echo to end (pin goes LOW)
        end_time = time.time()
        while lgpio.gpio_read(h, ECHO_PIN) == 1:
            end_time = time.time()
            if end_time > timeout:
                return None  # Timeout occurred
        
        # Calculate distance based on time of flight
        pulse_duration = end_time - start_time
        distance = (pulse_duration * 34300) / 2  # Speed of sound: 343 m/s
        
        return distance
        
    except Exception as e:
        print(f"Error measuring distance: {e}")
        return None

def is_dark():
    """
    Check if ambient light level is low using LDR sensor.
    
    Returns:
        bool: True if it's dark (LDR reads 1), False if there's light (LDR reads 0)
    """
    try:
        return lgpio.gpio_read(h, LDR_PIN) == 1
    except Exception as e:
        print(f"Error reading LDR sensor: {e}")
        return False

def detect_motion(current_distance):
    """
    Detect motion by comparing current distance with previous measurement.
    
    Args:
        current_distance (float): Current distance measurement in cm
        
    Returns:
        bool: True if motion is detected, False otherwise
    """
    global previous_distance
    
    if previous_distance is None:
        previous_distance = current_distance
        return False
    
    # Calculate the change in distance
    distance_change = abs(current_distance - previous_distance)
    
    # Update previous distance for next comparison
    previous_distance = current_distance
    
    # Motion detected if distance change exceeds threshold
    return distance_change > 5.0  # 5cm change threshold

def turn_on_lights():
    """
    Turn on all LEDs in the strip with the specified color.
    """
    global lights_on_until
    
    # Set all pixels to the motion detection color
    for i in range(NUM_PIXELS):
        pixels[i] = LED_COLOR
    
    pixels.show()
    
    # Set the time when lights should turn off
    lights_on_until = time.time() + LIGHT_ON_DURATION
    
    print("Motion detected in dark environment - Lights ON")

def turn_off_lights():
    """
    Turn off all LEDs in the strip.
    """
    # Set all pixels to black (off)
    pixels.fill(0x000000)
    pixels.show()
    
    print("Lights OFF")

def should_lights_be_on():
    """
    Check if lights should currently be on based on timer.
    
    Returns:
        bool: True if lights should be on, False otherwise
    """
    return time.time() < lights_on_until

def main():
    """
    Main program loop for motion detection system.
    """
    global lights_on_until
    
    print("Motion Detection System Starting...")
    print(f"Motion threshold: {MOTION_THRESHOLD} cm")
    print(f"Light duration: {LIGHT_ON_DURATION} seconds")
    print("Press Ctrl+C to exit")
    
    try:
        # Initialize with lights off
        turn_off_lights()
        
        while True:
            # Measure current distance
            distance = measure_distance()
            
            if distance is not None:
                # Check if object is within motion threshold
                object_detected = distance <= MOTION_THRESHOLD
                
                # Check ambient light level
                dark_environment = is_dark()
                
                # Print status information
                print(f"Distance: {distance:.1f}cm | Object detected: {object_detected} | Dark: {dark_environment}")
                
                # Turn on lights if object detected in dark environment
                if object_detected and dark_environment:
                    turn_on_lights()
                
                # Turn off lights if timer expired (mandatory after timeout)
                if not should_lights_be_on() and lights_on_until > 0:
                    turn_off_lights()
                    lights_on_until = 0
            
            else:
                print("Distance measurement failed")
                # Turn off lights if timer expired even with failed measurement
                if not should_lights_be_on() and lights_on_until > 0:
                    turn_off_lights()
                    lights_on_until = 0
            
            # Wait before next measurement
            time.sleep(MEASUREMENT_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nShutting down motion detection system...")
        
    finally:
        # Cleanup: turn off lights and close GPIO
        turn_off_lights()
        lgpio.gpiochip_close(h)
        print("System shutdown complete!")

if __name__ == "__main__":
    main()
