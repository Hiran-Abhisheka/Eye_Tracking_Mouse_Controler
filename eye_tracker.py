import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# MediaPipe indices for the eyes
# Left Eye landmarks: 362, 385, 387, 263, 373, 380
# Right Eye landmarks: 33, 160, 158, 133, 153, 144

# Function to calculate the eye aspect ratio (EAR)
def calculate_ear(landmarks, eye_indices):
    # Get the landmarks for the eye
    points = [landmarks[idx] for idx in eye_indices]
    
    # Calculate the horizontal distance
    horizontal_dist = np.linalg.norm(
        np.array([points[0].x, points[0].y]) - 
        np.array([points[3].x, points[3].y])
    )
    
    # Calculate the vertical distances
    vertical_dist1 = np.linalg.norm(
        np.array([points[1].x, points[1].y]) - 
        np.array([points[5].x, points[5].y])
    )
    vertical_dist2 = np.linalg.norm(
        np.array([points[2].x, points[2].y]) - 
        np.array([points[4].x, points[4].y])
    )
    
    # Average the vertical distances
    vertical_dist = (vertical_dist1 + vertical_dist2) / 2
    
    # Calculate EAR
    ear = vertical_dist / horizontal_dist if horizontal_dist > 0 else 0
    return ear

# Initialize video capture
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

# Set screen dimensions
screen_width, screen_height = pyautogui.size()

# Parameters for blink detection
BLINK_THRESHOLD = 0.2  # Adjust this threshold as needed
blink_counter = 0
blink_detected = False
last_blink_time = time.time()
BLINK_COOLDOWN = 0.5  # Seconds between blinks to avoid multiple clicks

# Smoothing parameters
smoothing_factor = 0.4  # Lower = more smoothing
prev_x, prev_y = 0, 0

# Font for text overlay
font = cv2.FONT_HERSHEY_SIMPLEX

# Calibration values (will be adjusted during runtime)
min_x, max_x = 0.4, 0.6
min_y, max_y = 0.4, 0.6
calibration_frames = 0
CALIBRATION_MAX_FRAMES = 30

# Calibration state
calibrating = True
calibration_points = []

while True:
    success, image = cap.read()
    if not success:
        print("Failed to capture frame")
        break
    
    # Flip the image horizontally for a mirror effect
    image = cv2.flip(image, 1)
    
    # Make a copy of the original image for display
    display_image = image.copy()
    
    # Convert to RGB for MediaPipe (it requires RGB input)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe
    results = face_mesh.process(image_rgb)
    
    # Enhance brightness and contrast of display image if needed
    alpha = 1.2  # Contrast control (1.0 means no change)
    beta = 10    # Brightness control (0 means no change)
    display_image = cv2.convertScaleAbs(display_image, alpha=alpha, beta=beta)
    
    # Get frame dimensions
    h, w, _ = image.shape
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the face mesh on the display image
            mp_drawing.draw_landmarks(
                image=display_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)
            
            # Get landmarks list
            landmarks = face_landmarks.landmark
            
            # Calculate EAR for both eyes
            left_eye_indices = [362, 385, 387, 263, 373, 380]
            right_eye_indices = [33, 160, 158, 133, 153, 144]
            
            left_ear = calculate_ear(landmarks, left_eye_indices)
            right_ear = calculate_ear(landmarks, right_eye_indices)
            
            # Average EAR
            avg_ear = (left_ear + right_ear) / 2
            
            # Display EAR value
            cv2.putText(display_image, f"EAR: {avg_ear:.2f}", (10, 30), font, 0.7, (0, 255, 0), 2)
            
            # Check for blink
            current_time = time.time()
            if avg_ear < BLINK_THRESHOLD:
                if not blink_detected and (current_time - last_blink_time) > BLINK_COOLDOWN:
                    blink_counter += 1
                    if blink_counter >= 2:  # Require 2 consecutive frames for a blink
                        blink_detected = True
                        last_blink_time = current_time
                        
                        # Perform click if not calibrating
                        if not calibrating:
                            pyautogui.click()
                            cv2.putText(display_image, "CLICK!", (w//2-50, h//2), font, 1, (0, 0, 255), 3)
            else:
                blink_counter = 0
                blink_detected = False
            
            # Get iris landmarks (left: 468, right: 473)
            left_iris = landmarks[468]
            right_iris = landmarks[473]
            
            # Average iris position (normalized to 0-1)
            iris_x = (left_iris.x + right_iris.x) / 2
            iris_y = (left_iris.y + right_iris.y) / 2
            
            # Draw iris positions
            left_iris_pos = (int(left_iris.x * w), int(left_iris.y * h))
            right_iris_pos = (int(right_iris.x * w), int(right_iris.y * h))
            cv2.circle(display_image, left_iris_pos, 3, (255, 0, 0), -1)
            cv2.circle(display_image, right_iris_pos, 3, (255, 0, 0), -1)
            
            # If calibrating, collect data points
            if calibrating:
                calibration_points.append((iris_x, iris_y))
                calibration_frames += 1
                
                # Display calibration progress
                cv2.putText(display_image, f"Calibrating: Look around the screen {calibration_frames}/{CALIBRATION_MAX_FRAMES}", 
                            (10, h-20), font, 0.7, (0, 255, 255), 2)
                
                if calibration_frames >= CALIBRATION_MAX_FRAMES:
                    # Calculate boundaries from collected data
                    x_values = [p[0] for p in calibration_points]
                    y_values = [p[1] for p in calibration_points]
                    
                    # Use percentiles to avoid outliers
                    min_x = np.percentile(x_values, 10) - 0.05
                    max_x = np.percentile(x_values, 90) + 0.05
                    min_y = np.percentile(y_values, 10) - 0.05
                    max_y = np.percentile(y_values, 90) + 0.05
                    
                    calibrating = False
            else:
                # Map iris position to screen coordinates with smoothing
                x_range = max_x - min_x
                y_range = max_y - min_y
                
                # Clamp values and map to screen
                clamped_x = max(min_x, min(iris_x, max_x))
                clamped_y = max(min_y, min(iris_y, max_y))
                
                # Map to screen coordinates
                mapped_x = (clamped_x - min_x) / x_range * screen_width
                mapped_y = (clamped_y - min_y) / y_range * screen_height
                
                # Apply smoothing
                smoothed_x = prev_x + smoothing_factor * (mapped_x - prev_x)
                smoothed_y = prev_y + smoothing_factor * (mapped_y - prev_y)
                
                # Update previous position
                prev_x, prev_y = smoothed_x, smoothed_y
                
                # Move the mouse
                pyautogui.moveTo(smoothed_x, smoothed_y)
                
                # Display calibration info
                cv2.putText(display_image, f"X: {iris_x:.2f} ({min_x:.2f}-{max_x:.2f})", 
                            (10, h-50), font, 0.6, (0, 255, 0), 2)
                cv2.putText(display_image, f"Y: {iris_y:.2f} ({min_y:.2f}-{max_y:.2f})", 
                            (10, h-30), font, 0.6, (0, 255, 0), 2)
    
    # Display instructions
    cv2.putText(display_image, "Press 'r' to recalibrate, 'q' to quit", (10, 60), font, 0.7, (255, 255, 255), 2)
    
    # Display the frame (use the original display image, not the processed one)
    cv2.imshow('Eye Tracking Mouse Control', display_image)
    
    # Key handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        # Reset calibration
        calibrating = True
        calibration_frames = 0
        calibration_points = []

# Release resources
cap.release()
cv2.destroyAllWindows()
