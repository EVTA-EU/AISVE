import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import time

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (800, 600)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLO model (DO NOT use export to NCNN here)
model = YOLO("model/yolov11_apple.pt")

# Detection loop
while True:
    # Capture frame
    frame = picam2.capture_array()
    
    # Run YOLO inference on the frame
    results = model(frame)
    
    # Create a copy of the frame for annotation
    annotated_frame = frame.copy()
    
    # Initialize variables to track the best detection
    best_label_text = ""
    
    # Process detection results
    for result in results:
        highest_conf = 0
        best_label = ""
        
        # Iterate through all detected boxes
        for box in result.boxes:
            # Get confidence score as percentage
            confidence = float(box.conf[0]) * 100
            
            # Only consider detections with confidence > 70% and higher than current best
            if confidence > 70 and confidence > highest_conf:
                cls_id = int(box.cls[0])  # Get class ID
                best_label = result.names[cls_id]  # Get class name
                highest_conf = confidence  # Update highest confidence
        
        # Format the best detection text if found
        if best_label:
            best_label_text = f"{best_label} {highest_conf:.2f}%"
    
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
    cv2.imshow("Camera", annotated_frame)
    
    # Exit when 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Clean up resources
cv2.destroyAllWindows()
