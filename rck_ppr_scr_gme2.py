import cv2
import random
import time
from collections import Counter
from module2 import find_position  # Assuming this finds hand positions

# Gesture mapping for Rock (0 fingers up), Paper (5 fingers up), and Scissors (2 fingers up)
gesture_dict = {
    (0, 0, 0, 0, 0): "Rock",      # No fingers up (fist)
    (1, 1, 1, 1, 1): "Paper",     # All fingers up (open hand)
    (0, 1, 1, 0, 0): "Scissors"   # Index and middle fingers up
}

# Rock Paper Scissors game logic
def get_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        return "You win!"
    else:
        return "Computer wins!"

# Ask user to play again using thumb up for yes and closed fist for no
def ask_user_to_play_again(hand_positions):
    if hand_positions:
        # Thumb up detection
        if hand_positions[4][1] < hand_positions[3][1]:  # Thumb is up
            return True  # Play again
        elif all(finger == 0 for finger in hand_positions):  # All fingers down (closed fist)
            return False  # Do not play again
    return None

# Initialize the video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Fingertip landmarks for index, middle, ring, pinky
tip_ids = [8, 12, 16, 20]

while True:
    print("Show thumbs up to start the game or closed fist to quit.")
    
    user_ready = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame_resized = cv2.resize(frame, (640, 480))  # Resize for performance
        hand_positions = find_position(frame_resized)

        if hand_positions:
            user_ready = ask_user_to_play_again(hand_positions)

            if user_ready is True:
                print("Starting the game...")
                break  # User is ready to play
            elif user_ready is False:
                print("Goodbye!")
                cap.release()
                cv2.destroyAllWindows()
                exit()

        cv2.imshow("Frame", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord("s"):  # Stop if 's' is pressed
            print("Stopping...")
            break

    # Start a 3-second countdown before drawing, showing the countdown on the screen
    countdown_start = time.time()
    countdown_duration = 3  # seconds
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame_resized = cv2.resize(frame, (640, 480))  # Resize for performance
        elapsed_time = time.time() - countdown_start
        remaining_time = countdown_duration - int(elapsed_time)
        
        if remaining_time <= 0:
            print("Start!")
            break

        # Overlay the countdown on the frame
        cv2.putText(frame_resized, str(remaining_time), (300, 240), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 4, cv2.LINE_AA)
        cv2.imshow("Frame", frame_resized)
        
        if cv2.waitKey(1) & 0xFF == ord("s"):
            print("Stopping...")
            break

    # Capture the user's gesture for Rock, Paper, Scissors
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame_resized = cv2.resize(frame, (640, 480))  # Resize for performance
    hand_positions = find_position(frame_resized)
    
    if hand_positions:
        fingers = []

        # Thumb detection: Compare thumb tip (ID 4) with base joint (ID 2)
        if hand_positions[4][1] < hand_positions[2][1]:  # Y-axis comparison
            fingers.append(1)  # Thumb is up
        else:
            fingers.append(0)  # Thumb is down

        # Check other fingers (index, middle, ring, pinky) based on vertical position (y-axis)
        fingers += [1 if hand_positions[tip][2] < hand_positions[tip - 2][2] else 0 for tip in tip_ids]

        # Check if the gesture is valid for Rock, Paper, or Scissors
        gesture = tuple(fingers)
        if gesture in gesture_dict:
            user_choice = gesture_dict[gesture]
            print(f"Your choice: {user_choice}")
            
            # Computer randomly chooses Rock, Paper, or Scissors
            computer_choice = random.choice(["Rock", "Paper", "Scissors"])
            print(f"Computer's choice: {computer_choice}")
            
            # Determine the winner
            result = get_winner(user_choice, computer_choice)
            print(f"Result: {result}")
        else:
            print("Gesture not recognized")
    else:
        print("No hand detected")

    cv2.imshow("Frame", frame_resized)
    
    # Ask the user if they want to play again
    print("Do you want to play again? Show thumbs up for yes or closed fist for no.")
    play_again = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame_resized = cv2.resize(frame, (640, 480))  # Resize for performance
        hand_positions = find_position(frame_resized)
        
        if hand_positions:
            play_again = ask_user_to_play_again(hand_positions)

            if play_again is True:
                print("Starting a new game...")
                break  # Restart the loop for a new game
            elif play_again is False:
                print("Thanks for playing!")
                cap.release()
                cv2.destroyAllWindows()
                exit()

        cv2.imshow("Frame", frame_resized)
        if cv2.waitKey(1) & 0xFF == ord("s"):  # Stop if 's' is pressed
            print("Stopping...")
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
