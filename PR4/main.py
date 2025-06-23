import cv2
import time
import board
import lgpio
import neopixel_spi as neopixel
import adafruit_ssd1306
from picamera2 import Picamera2
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import threading
import numpy as np

# ==================== PIN CONFIGURATION ====================
# Ultrasonic sensor
TRIGGER_PIN = 17
ECHO_PIN = 27

# LDR sensor
LDR_PIN = 22

# OLED Display (I2C)
OLED_WIDTH = 128
OLED_HEIGHT = 64

# ==================== LED STRIP CONFIGURATION ====================
NUM_PIXELS = 12
PIXEL_ORDER = neopixel.GRB
LED_COLOR = 0xFFFFFF
LED_BRIGHTNESS = 0.5

# ==================== DETECTION CONFIGURATION ====================
MOTION_THRESHOLD = 50.0  # cm
LIGHT_ON_DURATION = 10.0  # seconds
MEASUREMENT_INTERVAL = 0.2
CAMERA_TIMEOUT = 15.0  # Maximum time camera stays active
CLASSIFICATION_DELAY = 1.0  # Delay between classifications

# ==================== CLASSIFICATION CONFIGURATION ====================
# Mapping from YOLO model labels to our display categories
LABEL_MAPPING = {
    'plastic': 'PLASTIC',
    'paper': 'PAPER',
    'cardboard': 'CARDBOARD', 
    'organic': 'ORGANIC',
    'green-glass': 'GLASS'
}

class WasteClassificationSystem:
    def __init__(self):
        # Initialize GPIO
        self.h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(self.h, TRIGGER_PIN)
        lgpio.gpio_claim_input(self.h, ECHO_PIN)
        lgpio.gpio_claim_input(self.h, LDR_PIN)
        
        # Initialize LED strip
        spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(
            spi, 
            NUM_PIXELS, 
            brightness=LED_BRIGHTNESS,
            pixel_order=PIXEL_ORDER,
            auto_write=False
        )
        
        # Initialize OLED display
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=0x3C)
        self.oled.fill(0)
        self.oled.show()
        
        # Initialize camera and model once at startup
        self.initialize_camera_and_model()
        
        # State variables
        self.lights_on_until = 0
        self.camera_active_until = 0
        self.previous_distance = None
        self.last_classification = "WAITING..."
        self.classification_confidence = 0
        self.is_running = True
        self.last_classification_time = 0
        self.camera_lock = threading.Lock()
        self.camera_window_open = False
        
        # Show startup message
        self.display_startup_message()
        self.turn_off_lights()
        
    def display_startup_message(self):
        """Display startup message on screen"""
        image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        self.draw_centered_text(draw, "WASTE", font, -15)
        self.draw_centered_text(draw, "CLASSIFIER", font, 0)
        self.draw_centered_text(draw, "Starting...", font, 15)
        
        self.oled.image(image)
        self.oled.show()
        time.sleep(3)
        
    def draw_centered_text(self, draw, text, font, y_offset=0):
        """Draw horizontally centered text"""
        try:
            left, top, right, bottom = font.getbbox(text)
            font_width = right - left
            font_height = bottom - top
        except:
            # Fallback for older PIL versions
            font_width, font_height = font.getsize(text)
        
        x = (OLED_WIDTH - font_width) // 2
        y = (OLED_HEIGHT - font_height) // 2 + y_offset
        draw.text((x, y), text, font=font, fill=255)
        
    def measure_distance(self):
        """Measure distance using ultrasonic sensor"""
        try:
            lgpio.gpio_write(self.h, TRIGGER_PIN, 1)
            time.sleep(0.00001)
            lgpio.gpio_write(self.h, TRIGGER_PIN, 0)
            
            start_time = time.time()
            timeout = start_time + 0.1
            
            while lgpio.gpio_read(self.h, ECHO_PIN) == 0:
                start_time = time.time()
                if start_time > timeout:
                    return None
            
            end_time = time.time()
            while lgpio.gpio_read(self.h, ECHO_PIN) == 1:
                end_time = time.time()
                if end_time > timeout:
                    return None
            
            pulse_duration = end_time - start_time
            distance = (pulse_duration * 34300) / 2
            return distance
            
        except Exception as e:
            print(f"Error measuring distance: {e}")
            return None
    
    def is_dark(self):
        """Check if environment is dark"""
        try:
            return lgpio.gpio_read(self.h, LDR_PIN) == 1
        except Exception as e:
            print(f"Error reading LDR sensor: {e}")
            return False
    
    def detect_motion(self, current_distance):
        """Detect motion based on distance change"""
        if self.previous_distance is None:
            self.previous_distance = current_distance
            return False
        
        distance_change = abs(current_distance - self.previous_distance)
        self.previous_distance = current_distance
        
        return distance_change > 5.0
    
    def turn_on_lights(self):
        """Turn on LEDs"""
        try:
            for i in range(NUM_PIXELS):
                self.pixels[i] = LED_COLOR
            self.pixels.show()
            self.lights_on_until = time.time() + LIGHT_ON_DURATION
            print("Lights ON - Dark environment detected")
        except Exception as e:
            print(f"Error turning on lights: {e}")
    
    def turn_off_lights(self):
        """Turn off LEDs"""
        try:
            self.pixels.fill(0x000000)
            self.pixels.show()
        except Exception as e:
            print(f"Error turning off lights: {e}")
    
    def should_lights_be_on(self):
        """Check if lights should be on"""
        return time.time() < self.lights_on_until
    
    def initialize_camera_and_model(self):
        """Initialize camera and YOLO model once at startup"""
        try:
            print("Initializing camera...")
            self.picam2 = Picamera2()
            
            # Configure camera with proper settings
            config = self.picam2.create_preview_configuration(
                main={"size": (640, 480), "format": "RGB888"}
            )
            self.picam2.configure(config)
            self.picam2.start()
            
            # Wait for camera to stabilize
            time.sleep(2)
            
            # Load YOLO model with correct path
            print("Loading YOLO model...")
            self.model = YOLO("model/yolov11_garbage.pt")
            print("Camera and YOLO model initialized successfully")
            
        except Exception as e:
            print(f"Error initializing camera/model: {e}")
            self.picam2 = None
            self.model = None
    
    def classify_waste(self):
        """Classify waste using camera"""
        if self.picam2 is None or self.model is None:
            return
        
        # Limit classification frequency
        current_time = time.time()
        if current_time - self.last_classification_time < CLASSIFICATION_DELAY:
            return
        
        with self.camera_lock:
            try:
                # Capture frame
                frame = self.picam2.capture_array()
                
                if frame is None or frame.size == 0:
                    return
                
                # Show camera window when object is detected
                if not self.camera_window_open:
                    cv2.namedWindow('Waste Classifier Camera', cv2.WINDOW_AUTOSIZE)
                    self.camera_window_open = True
                
                # Run YOLO inference on the frame
                results = self.model(frame, verbose=False)
                
                # Create a copy of the frame for annotation
                annotated_frame = frame.copy()
                
                # Initialize variables to track the best detection
                best_label_text = ""
                best_category = ""
                highest_conf = 0
                
                # Process detection results
                for result in results:
                    if result.boxes is not None:
                        # Iterate through all detected boxes
                        for box in result.boxes:
                            # Get confidence score as percentage
                            confidence = float(box.conf[0]) * 100
                            
                            # Only consider detections with confidence > 60% and higher than current best
                            if confidence > 60 and confidence > highest_conf:
                                cls_id = int(box.cls[0])  # Get class ID
                                original_label = result.names[cls_id]  # Get original class name from model
                                
                                # Map the original label to our display category
                                if original_label in LABEL_MAPPING:
                                    best_category = LABEL_MAPPING[original_label]
                                    highest_conf = confidence  # Update highest confidence
                                    print(f"Detected: {original_label} -> Mapped to: {best_category}")  # Debug mapping
                
                # Format the best detection text if found
                if best_category:
                    best_label_text = f"{best_category} {highest_conf:.2f}%"
                    print(best_label_text)  # Print like your example
                    
                    self.last_classification = best_category
                    self.classification_confidence = highest_conf
                else:
                    self.last_classification = "UNIDENTIFIED"
                    self.classification_confidence = 0
                
                # Display the detection text on the frame
                if best_label_text:
                    cv2.putText(
                        annotated_frame,
                        best_label_text,
                        (30, 60),  # Position (x, y)
                        cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                        1.5,  # Font scale
                        (0, 0, 255),  # Color (BGR format - red)
                        3,  # Thickness
                        cv2.LINE_AA  # Anti-aliasing
                    )
                
                # Display the frame in a window
                cv2.imshow('Waste Classifier Camera', annotated_frame)
                cv2.waitKey(1)  # Refresh window
                
                self.last_classification_time = current_time
                        
            except Exception as e:
                print(f"Error: {e}")
                self.last_classification = "CAMERA ERROR"
                self.classification_confidence = 0
    
    def update_display(self):
        """Update OLED display with current information"""
        try:
            image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            
            # Title
            draw.text((30, 2), "CLASSIFIER", font=font, fill=255)
            
            # Current classification
            if self.classification_confidence > 0:
                draw.text((5, 18), f"Type: {self.last_classification}", font=font, fill=255)
                draw.text((5, 32), f"Conf: {self.classification_confidence:.1f}%", font=font, fill=255)
            else:
                self.draw_centered_text(draw, self.last_classification, font, 5)
            
            # System status
            current_time = time.time()
            if current_time < self.camera_active_until:
                draw.text((5, 46), "CAM: ACTIVE", font=font, fill=255)
            else:
                draw.text((5, 46), "CAM: IDLE", font=font, fill=255)
            
            # Light indicator
            if self.should_lights_be_on():
                draw.text((85, 46), "LED: ON", font=font, fill=255)
            else:
                draw.text((85, 46), "LED: OFF", font=font, fill=255)
            
            self.oled.image(image)
            self.oled.show()
            
        except Exception as e:
            print(f"Display update error: {e}")
    
    def sensor_monitoring_loop(self):
        """Main sensor monitoring loop"""
        print("Waste classification system started")
        print("Motion detection activated")
        
        while self.is_running:
            try:
                # Measure distance
                distance = self.measure_distance()
                
                if distance is not None:
                    object_detected = distance <= MOTION_THRESHOLD
                    dark_environment = self.is_dark()
                    
                    print(f"Distance: {distance:.1f}cm | Object: {object_detected} | Dark: {dark_environment}")
                    
                    # Activate camera if motion detected
                    if object_detected:
                        self.camera_active_until = time.time() + CAMERA_TIMEOUT
                    
                    # Turn on lights if dark and motion detected
                    if object_detected and dark_environment:
                        self.turn_on_lights()
                
                # Classify waste if camera should be active
                current_time = time.time()
                if current_time < self.camera_active_until and self.picam2 is not None:
                    self.classify_waste()
                elif current_time >= self.camera_active_until:
                    # Reset classification when camera becomes idle
                    if self.last_classification != "WAITING...":
                        self.last_classification = "WAITING..."
                        self.classification_confidence = 0
                        print("Camera idle - waiting for motion...")
                    
                    # Close camera window when idle
                    if self.camera_window_open:
                        cv2.destroyAllWindows()
                        self.camera_window_open = False
                
                # Manage lights
                if not self.should_lights_be_on() and self.lights_on_until > 0:
                    self.turn_off_lights()
                    self.lights_on_until = 0
                    print("Lights OFF")
                
                # Update display
                self.update_display()
                
                time.sleep(MEASUREMENT_INTERVAL)
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)
    
    def run(self):
        """Run the complete system"""
        try:
            self.sensor_monitoring_loop()
        except KeyboardInterrupt:
            print("\nStopping system...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        self.is_running = False
        
        try:
            # Clear display
            self.oled.fill(0)
            self.oled.show()
        except:
            pass
        
        try:
            # Close camera window
            if self.camera_window_open:
                cv2.destroyAllWindows()
        except:
            pass
        
        try:
            # Turn off lights
            self.turn_off_lights()
        except:
            pass
        
        try:
            # Stop camera
            if self.picam2 is not None:
                self.picam2.stop()
                self.picam2.close()
                self.picam2 = None
        except:
            pass
        
        try:
            # Close GPIO
            lgpio.gpiochip_close(self.h)
        except:
            pass
        
        print("System completely stopped")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    system = WasteClassificationSystem()
    system.run()
