import time
import board
import adafruit_dht
import adafruit_ssd1306
import lgpio
from PIL import Image, ImageDraw, ImageFont

# Pin definitions
DHT_PIN = board.D4          # DHT11 temperature and humidity sensor
LDR_PIN = 17               # Light sensor
BUTTON_MODE = 23           # Single button to cycle display modes

# OLED display dimensions
WIDTH = 128
HEIGHT = 64

# Initialize sensors and display
dht = adafruit_dht.DHT11(DHT_PIN)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Initialize GPIO
h = lgpio.gpiochip_open(0)

# Set up GPIO pins
lgpio.gpio_claim_input(h, LDR_PIN)
lgpio.gpio_claim_input(h, BUTTON_MODE, lgpio.SET_PULL_UP)

# Display modes
MODE_TEMP = 0
MODE_HUMIDITY = 1
MODE_LIGHT = 2
MODE_ALL = 3

class EnvironmentalStation:
    def __init__(self):
        self.current_mode = MODE_ALL
        self.temperature = None
        self.humidity = None
        self.light_level = "Unknown"
        self.last_button_time = 0
        self.button_debounce = 0.3  # 300ms debounce
        
        # Clear display
        oled.fill(0)
        oled.show()
        
    def read_sensors(self):
        """Read all sensor values"""
        # Read temperature and humidity
        try:
            self.temperature = dht.temperature
            self.humidity = dht.humidity
        except RuntimeError as e:
            print(f"DHT sensor error: {e.args[0]}")
            
        # Read light sensor
        light_reading = lgpio.gpio_read(h, LDR_PIN)
        
        # Determine light level based on sensor reading
        if light_reading == 0:
            self.light_level = "Bright"
        else:
            self.light_level = "Dark"
            
    def check_buttons(self):
        """Check button press with debouncing"""
        current_time = time.time()
        
        if current_time - self.last_button_time < self.button_debounce:
            return
            
        if lgpio.gpio_read(h, BUTTON_MODE) == 0:
            # Cycle through modes: ALL -> TEMP -> HUMIDITY -> LIGHT -> ALL
            self.current_mode = (self.current_mode + 1) % 4
            self.last_button_time = current_time
            
            mode_names = ["All Data", "Temperature", "Humidity", "Light"]
            print(f"{mode_names[self.current_mode]} mode selected")
            
    def get_font_size(self, font, text):
        """Calculate text dimensions"""
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top
        
    def draw_centered_text(self, draw, text, font, y_offset=0):
        """Draw text centered horizontally"""
        font_width, font_height = self.get_font_size(font, text)
        x = (WIDTH - font_width) // 2
        y = (HEIGHT - font_height) // 2 + y_offset
        draw.text((x, y), text, font=font, fill=255)
        
    def display_temperature(self):
        """Display temperature screen"""
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Title
        self.draw_centered_text(draw, "TEMPERATURE", font, -20)
        
        # Temperature value
        if self.temperature is not None:
            temp_text = f"{self.temperature}°C"
            # Check comfort level
            if self.temperature < 18:
                comfort = "Cold"
            elif self.temperature > 26:
                comfort = "Hot"
            else:
                comfort = "Comfortable"
                
            self.draw_centered_text(draw, temp_text, font, 0)
            self.draw_centered_text(draw, comfort, font, 15)
        else:
            self.draw_centered_text(draw, "Sensor Error", font, 0)
            
        oled.image(image)
        oled.show()
        
    def display_humidity(self):
        """Display humidity screen"""
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Title
        self.draw_centered_text(draw, "HUMIDITY", font, -20)
        
        # Humidity value
        if self.humidity is not None:
            humidity_text = f"{self.humidity}%"
            
            # Check humidity level
            if self.humidity < 30:
                level = "Dry"
            elif self.humidity > 70:
                level = "Humid"
            else:
                level = "Optimal"
                
            self.draw_centered_text(draw, humidity_text, font, 0)
            self.draw_centered_text(draw, level, font, 15)
        else:
            self.draw_centered_text(draw, "Sensor Error", font, 0)
            
        oled.image(image)
        oled.show()
        
    def display_light(self):
        """Display light information screen"""
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Title
        self.draw_centered_text(draw, "LIGHT LEVEL", font, -20)
        
        # Light level
        self.draw_centered_text(draw, self.light_level, font, 0)
        
        # Energy saving tip
        if "Dark" in self.light_level:
            tip = "Turn on lights"
        elif "Bright" in self.light_level:
            tip = "Good lighting"
        else:
            tip = "Adequate lighting"
            
        self.draw_centered_text(draw, tip, font, 15)
        
        oled.image(image)
        oled.show()
        
    def display_all_data(self):
        """Display all sensor data on one screen"""
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Title
        draw.text((35, 2), "ENV MONITOR", font=font, fill=255)
        
        # Temperature
        if self.temperature is not None:
            temp_text = f"T: {self.temperature}°C"
        else:
            temp_text = "T: Error"
        draw.text((5, 18), temp_text, font=font, fill=255)
        
        # Humidity
        if self.humidity is not None:
            hum_text = f"H: {self.humidity}%"
        else:
            hum_text = "H: Error"
        draw.text((5, 32), hum_text, font=font, fill=255)
        
        # Light
        light_text = f"L: {self.light_level}"
        if len(light_text) > 16:  # Truncate if too long
            light_text = light_text[:13] + "..."
        draw.text((5, 46), light_text, font=font, fill=255)
        
        # Instructions
        # draw.text((5, 58), "Press button to cycle", font=font, fill=255)
        
        oled.image(image)
        oled.show()
        
    def update_display(self):
        """Update display based on current mode"""
        if self.current_mode == MODE_TEMP:
            self.display_temperature()
        elif self.current_mode == MODE_HUMIDITY:
            self.display_humidity()
        elif self.current_mode == MODE_LIGHT:
            self.display_light()
        else:  # MODE_ALL
            self.display_all_data()
            
    def run(self):
        """Main monitoring loop"""
        print("Environmental Monitoring Station Started")
        print("Press button to cycle through display modes:")
        print("- All Data -> Temperature -> Humidity -> Light -> All Data")
        
        # Show startup message
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        self.draw_centered_text(draw, "ENV STATION", font, -10)
        self.draw_centered_text(draw, "Starting...", font, 10)
        oled.image(image)
        oled.show()
        time.sleep(2)
        
        while True:
            try:
                # Read all sensors
                self.read_sensors()
                
                # Check for button presses
                self.check_buttons() 
                
                # Update display
                self.update_display()
                
                # Brief delay before next update
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\nShutting down Environmental Station...")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

# Create and run the environmental station
if __name__ == "__main__":
    station = EnvironmentalStation()
    
    try:
        station.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        # Cleanup
        print("Cleaning up GPIO...")
        oled.fill(0)  # Clear display
        oled.show()
        lgpio.gpiochip_close(h)  # Close GPIO
        print("Environmental Station shutdown complete.")
