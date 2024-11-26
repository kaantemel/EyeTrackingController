
# Eye Tracking Controller for ALS Patients

This project provides an eye-tracking-based controller designed to assist ALS (Amyotrophic Lateral Sclerosis) patients in interacting with applications. The system leverages computer vision techniques to detect eye gaze direction and blinking patterns for selecting and interacting with a virtual grid.

## Features
- **Eye Gaze Detection**: Tracks gaze direction to navigate through a 4x4 grid interface.
- **Blink Detection**: Detects blinking to confirm selection of grid cells.
- **User-Friendly Interface**: Visual feedback on cell highlighting and selections.
- **Non-Invasive**: Requires only a webcam for operation.

## How It Works
1. **Face and Eye Detection**: Uses `dlib` for detecting facial landmarks.
2. **Blink Ratio**: Calculates the eye aspect ratio to identify blinks.
3. **Gaze Ratio**: Computes gaze direction based on eye positioning and adjusts the highlighted cell.
4. **Grid Interaction**: Highlights grid cells based on gaze direction and selects them upon detecting a series of blinks.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/eye-tracking-controller.git
   cd eye-tracking-controller
   ```

2. **Install Dependencies**
   Ensure you have Python 3.7 or later installed. Install the required Python libraries:
   ```bash
   pip install opencv-python numpy dlib
   ```

3. **Download the Required Model**
   Download the `shape_predictor_68_face_landmarks.dat` file from [dlib's model repository](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and place it in the project directory.

4. **Run the Application**
   ```bash
   python EyeTrackingController.py
   ```

## Usage
- Position yourself in front of the webcam.
- Use your gaze to navigate the grid:
  - **Right Movement**: Gaze left.
  - **Left Movement**: Gaze right.
- Blink three times consecutively to select a highlighted cell.

## Requirements
- **Hardware**: Webcam-enabled device.
- **Software**:
  - Python 3.7 or later
  - OpenCV
  - NumPy
  - dlib

## Limitations
- Requires a well-lit environment for accurate detection.
- May need calibration for different lighting and facial features.

## Future Improvements
- Add support for more complex grids.
- Improve robustness in varying lighting conditions.
- Implement a calibration routine for different users.
