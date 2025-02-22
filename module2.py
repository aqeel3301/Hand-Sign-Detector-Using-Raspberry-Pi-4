import cv2
import mediapipe as mp
from gtts import gTTS
import os

# Initialize mediapipe hand and drawing modules
drawing_utils = mp.solutions.drawing_utils
hands_module = mp.solutions.hands
hands = hands_module.Hands()

h, w = 480, 640  # Frame height and width

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

# Function to find hand landmarks' positions
def find_position(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    positions = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            drawing_utils.draw_landmarks(frame, hand_landmarks, hands_module.HAND_CONNECTIONS)
            for id, landmark in enumerate(hand_landmarks.landmark):
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                positions.append([id, x, y])

    return positions

# Function to find names of landmarks
def find_landmark_names():
    landmarks_names = [landmark.name.replace("_", " ") for landmark in mp.solutions.hands.HandLandmark]
    return landmarks_names
