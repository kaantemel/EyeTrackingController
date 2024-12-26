import cv2
import numpy as np
import dlib
from math import hypot
import time

# Initialize video capture on the default camera
cap = cv2.VideoCapture(0)
# Initialize face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to calculate the midpoint between two points
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

# Font for displaying text on the video frame
font = cv2.FONT_HERSHEY_SIMPLEX

# Function to calculate the ratio of the horizontal and vertical lengths of the eye
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_length / ver_line_length
    return ratio

# Function to calculate the gaze ratio based on the white part of the eyes
def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

# Initial setup for control indices and timing
highlighted_control_index = 0
highlighted_cell_index = 0
grid_size = (1, 3)
frame_width = 1000
cell_width = frame_width // 3
cell_height = 120
labels = ['TV', 'Radio', 'Light']

last_update_time = time.time()
minimum_blink_interval = 0.2
update_delay = 0.5
gaze_lock_duration = 1.5
last_gaze_update_lock_time = 0
new_count = time.time()

blink_count = 0
last_blink_time = time.time()
blink_detection_threshold = 5.0
selection_made = False
current_mode = 'main'
device_controls = {
    'TV': ['Ch UP', ' Ch. DOWN', 'Vol UP', 'Vol DOWN', 'ON/OFF', 'BACK'],
    'Radio': ['Rd UP', 'Rd DOWN', 'Vol UP', 'Vol DOWN', 'ON/OFF', 'BACK'],
    'Light': ['ON', 'OFF','BACK']
}

background_color = (50, 50, 50)  # Main menu background color

# Main video processing loop
while True:
    _, frame = cap.read()
    new_frame = np.zeros((cell_height, frame_width, 3), dtype=np.uint8)
    new_frame[:] = background_color  # Uniform background color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_time = time.time()

    # Display main menu or device controls based on the current mode
    if current_mode == 'main':
        for j in range(grid_size[1]):
            top_left = (j * cell_width, 0)
            bottom_right = ((j + 1) * cell_width, cell_height)
            color = background_color if j == highlighted_cell_index else (200, 200, 200)
            cv2.rectangle(new_frame, top_left, bottom_right, color, -1)
            text = labels[j]
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = top_left[0] + (cell_width - text_size[0]) // 2
            text_y = top_left[1] + (cell_height + text_size[1]) // 2
            cv2.putText(new_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
    else:
        controls = device_controls[current_mode]
        control_width = frame_width // len(controls)
        for i, control in enumerate(controls):
            text_size = cv2.getTextSize(control, font, 1, 2)[0]
            text_x = i * control_width + (control_width - text_size[0]) // 2
            text_y = cell_height // 2 + text_size[1] // 2
            color = background_color if i == highlighted_control_index else (200, 200, 200)
            cv2.rectangle(new_frame, (i * control_width, 0), ((i + 1) * control_width, cell_height), color, -1)
            cv2.putText(new_frame, control, (text_x, text_y), font, 1, (255, 255, 255), 2)

    # Detect faces, calculate gaze and blinking ratios, and update control index accordingly
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        gaze_ratio = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks) + get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio /= 2
        blinking_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks) + get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio /= 2

        if blinking_ratio > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))
            last_gaze_update_lock_time = current_time
            if current_time - last_blink_time <= blink_detection_threshold and current_time - last_blink_time > minimum_blink_interval:
                blink_count += 1
            else:
                blink_count = 0
                selection_made = False
            last_blink_time = current_time
            if blink_count >= 3:
                if current_mode == 'main':
                    current_mode = labels[highlighted_cell_index]
                    highlighted_control_index = 0  # Reset control index on entering a mode
                    blink_count = 0
                else:
                    print(f"{controls[highlighted_control_index]} button is selected")
                    if(controls[highlighted_control_index]=='BACK'):
                        print('else will be https')
                    current_mode = 'main'
                    selection_made = True
                    blink_count = 0
                new_count = current_time

        if current_mode != 'main' and current_time - last_gaze_update_lock_time > gaze_lock_duration:
            if gaze_ratio <= 1:
                highlighted_control_index = (highlighted_control_index + 1) % len(device_controls[current_mode])
                last_gaze_update_lock_time = current_time
                blink_count = 0
            elif gaze_ratio > 1.7:
                highlighted_control_index = (highlighted_control_index - 1) % len(device_controls[current_mode])
                last_gaze_update_lock_time = current_time
                blink_count = 0
        if current_mode == 'main' and current_time - last_gaze_update_lock_time > gaze_lock_duration:
            if gaze_ratio <= 1:
                highlighted_cell_index = (highlighted_cell_index + 1) % 3
                last_gaze_update_lock_time = current_time
                blink_count = 0
            elif gaze_ratio > 1.7:
                highlighted_cell_index = (highlighted_cell_index - 1) % 3
                last_gaze_update_lock_time = current_time
                blink_count = 0

    # Display the video and interface frames
    cv2.imshow("Frame", frame)
    cv2.imshow("New Frame", new_frame)

    # Check for 'ESC' key to exit the loop
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
