import cv2
import numpy as np
import dlib
from math import hypot
import time

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_length / ver_line_length
    return ratio

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

grid_size = (4, 4)
cell_width = 100
cell_height = 120
highlighted_cell_index = 0

last_update_time = time.time()
update_delay = 1.0
blink_lock_time = 1.0
last_blink_lock_time = 0

blink_count = 0
last_blink_time = time.time()
blink_detection_threshold = 4

while True:
    _, frame = cap.read()
    new_frame = np.zeros((480, 400, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            cell_num = i * grid_size[1] + j + 1
            top_left = (j * cell_width, i * cell_height)
            bottom_right = ((j + 1) * cell_width, (i + 1) * cell_height)
            color = (100, 100, 100) if cell_num - 1 == highlighted_cell_index else (200, 200, 200)
            cv2.rectangle(new_frame, top_left, bottom_right, color, -1)
            cv2.putText(new_frame, str(cell_num), (top_left[0] + 20, top_left[1] + 70), font, 2, (255, 255, 255), 2)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        gaze_ratio = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks) + get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio /= 2

        current_time = time.time()
        if current_time - last_update_time > update_delay and current_time - last_blink_lock_time > blink_lock_time:
            if gaze_ratio <= 1:
                highlighted_cell_index = (highlighted_cell_index + 1) % 16
            elif gaze_ratio > 1.7:
                highlighted_cell_index = (highlighted_cell_index - 1) % 16
            last_update_time = current_time

        blinking_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks) + get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio /= 2

        if blinking_ratio > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))
            last_blink_lock_time = current_time  # Lock highlight movement
            if current_time - last_blink_time <= blink_detection_threshold:
                blink_count += 1
                if blink_count >= 3:
                    print(f"Cell {highlighted_cell_index + 1} selected")
                    blink_count = 0  # Reset after action
            else:
                blink_count = 1
            last_blink_time = current_time

    cv2.imshow("Frame", frame)
    cv2.imshow("New Frame", new_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
