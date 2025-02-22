import cv2
from collections import Counter
from module2 import find_landmark_names, find_position

# Dictionary to map finger combinations to words/letters
gesture_dict = {
    (1, 1, 0, 0, 0): "A",               # Thumb and Index up
    (0, 1, 1, 1, 1): "B",               # All fingers except thumb up
    (1, 0, 0, 0, 0): "Thumb Up",        # Thumb only
    (1, 1, 1, 1, 1): "Hello",           # All fingers up
    (0, 0, 0, 0, 0): "No fingers up",   # All fingers down
    (0, 1, 1, 0, 0): "Victory",         # Index and Middle fingers up
    (0, 0, 1, 0, 0): "Middle finger up",# Only Middle finger up
    (1, 0, 1, 0, 0): "Surfer",          # Thumb and Middle finger up
    (0, 1, 0, 0, 0): "Index Up",        # Only Index finger up
    (0, 0, 0, 1, 0): "Ring Up",         # Only Ring finger up
    (0, 0, 0, 0, 1): "Pinky Up",        # Only Pinky finger up
    (1, 1, 0, 0, 1): "Wassup",
    (1, 1, 1, 0, 0): "C",
}

# Initialize the video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Fingertip landmarks for index, middle, ring, pinky
tip_ids = [8, 12, 16, 20]

# Infinite loop for live feed and hand detection
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    #frame = cv2.flip(frame,0)

    frame_resized = cv2.resize(frame, (640, 480))  # Resize for performance
    
    # Get hand landmark positions
    hand_positions = find_position(frame_resized)
    
    # Get landmark names (no argument needed)
    landmark_names = find_landmark_names()
    
    if hand_positions and landmark_names:
        fingers = []

        # Thumb: check based on horizontal position (x-axis)
        thumb_up = 1 if hand_positions[4][1] < hand_positions[2][1] else 0
        fingers.append(thumb_up)

        # Check other fingers (index, middle, ring, pinky) based on vertical position (y-axis)
        for i, tip_id in enumerate(tip_ids):
            # Compare fingertip position with the joint position to determine if the finger is up
            if hand_positions[tip_id][2] < hand_positions[tip_id - 2][2]:  # Y-axis comparison
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is down

        # Convert the list to a tuple for dictionary lookup
        gesture = tuple(fingers)

        # Check if the detected gesture matches any in the gesture dictionary
        if gesture in gesture_dict:
            recognized_word = gesture_dict[gesture]
            print(f"Gesture recognized: {recognized_word}")
        else:
            print("Gesture not recognized")
    else:
        print("No hand detected")

    # Display the camera frame with the current detection
    cv2.imshow("Frame", frame_resized)
    
    # Stop the loop if the user presses 's'
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        print("Stopping...")
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
