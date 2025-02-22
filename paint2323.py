import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe hands module
handsModule = mp.solutions.hands

# Initialize video capture
cap = cv2.VideoCapture(0)

# Confidence values and settings for hand tracking
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    # Create a black canvas to draw on, the same size as the frames from the camera
    canvas = None
    prev_x, prev_y = None, None  # Previous position of the index finger

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        
        # Resize the frame for performance
        frame1 = cv2.resize(frame, (640, 480))
        
        # Initialize canvas if it is None (first loop)
        if canvas is None:
            canvas = np.zeros_like(frame1)  # Black canvas to draw on

        # Process the frame for hand landmarks
        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
        
        # If hand landmarks are found, track only the index finger (no drawing hand framework)
        if results.multi_hand_landmarks is not None:
            for handLandmarks in results.multi_hand_landmarks:
                # Find the location of the index finger (landmark 8)
                index_finger_tip = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP]
                index_x, index_y = int(index_finger_tip.x * 640), int(index_finger_tip.y * 480)
                
                # If previous index finger position exists, draw a white line
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), (255, 255, 255), 5)
                
                # Update the previous position to current position
                prev_x, prev_y = index_x, index_y
        else:
            # Reset previous position if no hand is detected
            prev_x, prev_y = None, None
        
        # Combine the canvas and the current frame
        frame_with_drawing = cv2.add(frame1, canvas)
        
        # Show the output
        cv2.imshow("Frame", frame_with_drawing)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):  # Stop if 'q' is pressed
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
