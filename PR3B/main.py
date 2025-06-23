import cv2
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO
import time
import os

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (800, 600)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the custom YOLO segmentation model
print("Loading segmentation model...")
model = YOLO("model/yolov11_seg_trash.pt")
print("✅ Model loaded successfully")

# Configure parameters
conf_threshold = 0.01  # Confidence threshold
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), 
          (0, 255, 255), (128, 0, 128), (255, 165, 0), (255, 192, 203), (165, 42, 42)]

print("Starting real-time detection. Press 'q' to exit...")

try:
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        
        # Convert from RGB to BGR for OpenCV (if necessary)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        img_height, img_width = frame_bgr.shape[:2]
        
        # Run YOLO inference
        results = model(frame_bgr, conf=conf_threshold, verbose=False)
        
        # Create copy for overlay
        overlay = frame_bgr.copy()
        
        # Process results following your successful method
        for result in results:
            # Check if there are masks and detections
            if result.masks is not None and len(result.masks) > 0:
                # Get mask data, boxes and confidences
                masks = result.masks.data.cpu().numpy()
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_indices = result.boxes.cls.cpu().numpy()
                
                print(f"Detected {len(masks)} masks")
                
                # Process each prediction
                for i, (mask, box, conf, cls_idx) in enumerate(zip(masks, boxes, confidences, class_indices)):
                    if conf > conf_threshold:
                        # Resize mask to image size
                        mask_resized = cv2.resize(mask, (img_width, img_height))
                        
                        # Get color for this class
                        color = np.array(colors[int(cls_idx) % len(colors)])
                        
                        # Create colored mask overlay (exact method from your function)
                        mask_indices = mask_resized > 0.5
                        overlay[mask_indices] = overlay[mask_indices] * 0.6 + color * 0.4
                        
                        # Draw bounding box
                        x1, y1, x2, y2 = box.astype(int)
                        cv2.rectangle(overlay, (x1, y1), (x2, y2), color.tolist(), 2)
                        
                        # Get class name
                        class_name = result.names[int(cls_idx)] if hasattr(result, 'names') else f"Class {int(cls_idx)}"
                        
                        # Add label with confidence
                        label = f"{class_name}: {conf:.2f}"
                        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                        
                        # Background for text
                        cv2.rectangle(overlay, (x1, y1-text_height-10), (x1+text_width, y1), color.tolist(), -1)
                        cv2.putText(overlay, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        
                        # Optional: draw contours for better definition
                        mask_binary = (mask_resized > 0.5).astype(np.uint8)
                        contours, _ = cv2.findContours(mask_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        cv2.drawContours(overlay, contours, -1, color.tolist(), 2)
            
            else:
                # If there are detections but no masks (only bounding boxes)
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    class_indices = result.boxes.cls.cpu().numpy()
                    
                    for box, conf, cls_idx in zip(boxes, confidences, class_indices):
                        if conf > conf_threshold:
                            x1, y1, x2, y2 = box.astype(int)
                            color = colors[int(cls_idx) % len(colors)]
                            
                            # Draw only bounding box if no masks available
                            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)
                            
                            class_name = result.names[int(cls_idx)] if hasattr(result, 'names') else f"Class {int(cls_idx)}"
                            label = f"{class_name}: {conf:.2f}"
                            cv2.putText(overlay, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Display frame with overlays
        cv2.imshow("YOLO Segmentation", overlay)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break

except KeyboardInterrupt:
    print("\nInterrupted by user")
except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up resources
    print("Closing application...")
    picam2.stop()
    cv2.destroyAllWindows()
    print("✅ Resources freed successfully")
