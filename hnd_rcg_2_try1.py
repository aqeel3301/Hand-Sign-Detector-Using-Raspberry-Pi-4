import cv2
from collections import Counter
from module2 import find_landmark_names, find_position

gesture_dict = {
    (1, 1, 0, 0, 0): "A",               
    (0, 1, 1, 1, 1): "B",               
    (1, 0, 0, 0, 0): "Thumb Up",        
    (1, 1, 1, 1, 1): "Hello",           
    (0, 0, 0, 0, 0): "No fingers up",   
    (0, 1, 1, 0, 0): "Victory",         
    (0, 0, 1, 0, 0): "Middle finger up",
    (1, 0, 1, 0, 0): "Surfer",          
    (0, 1, 0, 0, 0): "Index Up",        
    (0, 0, 0, 1, 0): "Ring Up",         
    (0, 0, 0, 0, 1): "Pinky Up",        
    (1, 1, 0, 0, 1): "Wassup",
    (1, 1, 1, 0, 0): "C",
}

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

tip_ids = [8, 12, 16, 20]
last_gesture = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame_resized = cv2.resize(frame, (640, 480))
    hand_positions = find_position(frame_resized)
    landmark_names = find_landmark_names()
    
    if hand_positions and landmark_names:
        fingers = []

        thumb_up = 1 if hand_positions[4][1] < hand_positions[2][1] else 0
        fingers.append(thumb_up)

        for i, tip_id in enumerate(tip_ids):
            if hand_positions[tip_id][2] < hand_positions[tip_id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        gesture = tuple(fingers)

        if gesture != last_gesture:
            if gesture in gesture_dict:
                recognized_word = gesture_dict[gesture]
                print(f"Gesture recognized: {recognized_word}")
                cv2.putText(frame_resized, recognized_word, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                recognized_word = "Gesture not recognized"
                cv2.putText(frame_resized, recognized_word, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            last_gesture = gesture
    else:
        cv2.putText(frame_resized, "No hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Frame", frame_resized)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        print("Stopping...")
        break

cap.release()
cv2.destroyAllWindows()
