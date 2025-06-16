import lgpio
import time

# GPIO pin definitions
SERVO_PIN = 27      # Pin for the servo motor
LDR_PIN_LEFT = 17   # Pin for the left LDR (Light Dependent Resistor) sensor
LDR_PIN_RIGHT = 22  # Pin for the right LDR sensor

# Initialize the GPIO chip (default GPIO chip is usually "/dev/gpiochip0")
h = lgpio.gpiochip_open(0)

# Claim the GPIO pins for use
lgpio.gpio_claim_output(h, SERVO_PIN)      # Set servo pin as output
lgpio.gpio_claim_input(h, LDR_PIN_LEFT)    # Set left LDR pin as input
lgpio.gpio_claim_input(h, LDR_PIN_RIGHT)   # Set right LDR pin as input

# Function to generate PWM signal for servo motor control
def set_servo_pulsewidth(h, pin, pulse_width):
    """
    Sends a HIGH signal to the servo pin for the specified pulse width (in milliseconds).
    This creates a PWM signal by keeping the pin HIGH for a specific duration.
    
    Args:
        h: GPIO chip handle
        pin: GPIO pin number for the servo
        pulse_width: Duration of the pulse in milliseconds (typically 1-2ms for servos)
    """
    lgpio.gpio_write(h, pin, 1)        # Set pin HIGH (start of pulse)
    time.sleep(pulse_width / 1000)     # Wait for pulse duration
    lgpio.gpio_write(h, pin, 0)        # Set pin LOW (end of pulse)

# Function to move servo to a specific angle
def move_servo(angle):
    """
    Converts the given angle (between 0 and 180 degrees) to corresponding pulse width
    and moves the servo to that position.
    
    Standard servo control:
    - 0 degrees = 1ms pulse width
    - 90 degrees = 1.5ms pulse width  
    - 180 degrees = 2ms pulse width
    
    Args:
        angle: Target angle in degrees (0-180)
    """
    pulse_width = 1 + (angle / 180.0)  # Calculate pulse width (1ms to 2ms range)
    set_servo_pulsewidth(h, SERVO_PIN, pulse_width)  # Send PWM signal to move servo

# Main control loop - servo follows light detected by LDR sensors
try:
    while True:
        # Read current state of left and right LDR sensors
        # Note: LDR sensors typically output LOW (0) when light is detected
        light_left = lgpio.gpio_read(h, LDR_PIN_LEFT)
        light_right = lgpio.gpio_read(h, LDR_PIN_RIGHT)
        
        # Decision logic based on light sensor readings (45-degree increments)
        if light_left == 0 and light_right == 0:
            # Light detected on both sides - move to center position
            print("Light detected on both sides! Moving servo to straight position.")
            move_servo(90)  # Move servo to center position (90 degrees)
            
        elif light_left == 0:
            # Light detected only on left side - turn left
            print("Light detected on the left! Moving servo towards the left.")
            move_servo(45)  # Move servo to 45 degrees (left position)
            
        elif light_right == 0:
            # Light detected only on right side - turn right
            print("Light detected on the right! Moving servo towards the right.")
            move_servo(135) # Move servo to 135 degrees (right position)
            
        else:
            # No light detected on either side - maintain center position
            print("No light detected on either side! Keeping servo in straight position.")
            move_servo(90)  # Move servo to center position (90 degrees)
        
        # Short delay to prevent continuous readings and allow time for changes
        time.sleep(1)

except KeyboardInterrupt:
    # Handle user interruption (Ctrl + C) to stop the program gracefully
    print("\nStopping servo control and exiting program.")

finally:
    # Clean up and close GPIO resources before exiting the program
    lgpio.gpio_write(h, SERVO_PIN, 0)  # Turn off SERVO_PIN before exiting
    lgpio.gpiochip_close(h)            # Close the GPIO chip
    print("GPIO cleaned up and resources released.")
