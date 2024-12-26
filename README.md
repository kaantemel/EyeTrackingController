
# Eye Tracking Controller for ALS Patients

This repository contains the implementation of an eye-tracking system designed for ALS patients to control various room functions (like lights, TV, and radio) using eye movements. The system utilizes standard webcams and operates on general-purpose computers, requiring no specialized hardware.

## Project Overview
Patients with Amyotrophic Lateral Sclerosis (ALS) often face significant mobility challenges, primarily relying on eye movements for communication and interaction. This project aims to empower these patients by enabling them to control a smart home environment through eye tracking.

## Features
- **Eye and Blink Detection**: Utilizes OpenCV and Dlib to detect the user's eye movements and blinks accurately.
- **Horizontal Gaze Interaction**: Tracks horizontal eye movements to navigate through a grid-based interface.
- **Blink-Based Interaction**: Employs blink detection for making selections, minimizing false activations.
- **Simple, Grid-Based UI**: Features a straightforward interface that's easy to navigate using eye movements.

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

## Usage Demonstration
### The Demo
![Adsztasarm1-ezgif com-optimize](https://github.com/user-attachments/assets/35b0a035-1c6f-4d01-b5ad-3f5f7f4bfef2)
### The Output
![alt text](https://i.imgur.com/RwNFWHx.jpeg)

## User Interface
### Main Menu
The main menu provides three options:
- TV
- Radio
- Light
  
![alt text](https://i.imgur.com/fhbiHyT.png)

### Submenu: TV Controls
Options available:
- Channel Up
- Channel Down
- Volume Up
- Volume Down
- On/Off
- Back to Main Menu

![alt text](https://i.imgur.com/ccxChlx.png)

### Submenu: Radio Controls
Options available:
- Radio Up
- Radio Down
- Volume Up
- Volume Down
- On/Off
- Back to Main Menu
  
![alt text](https://i.imgur.com/IyCSO2l.png)

### Submenu: Light Controls
Options available:
- On
- Off
- Back to Main Menu

![alt text](https://i.imgur.com/oeawb11.png)

## Requirements
- **Hardware**: Webcam-enabled device.
- **Software**:
  - Python 3.7 or later
  - OpenCV
  - NumPy
  - dlib

## Further Improvements
- **HTTP Requests**: Currently, the system prints out commands based on eye movements and blinks. Future implementations will include sending HTTP requests to a server or devices to execute the commands in a smart home setup, allowing for real control over home appliances.
- **Lock System**: To enhance usability and prevent unintended selections, a locking mechanism will be integrated. This lock system will require a specific, deliberate action, such as a longer gaze or a sequence of blinks, to unlock command execution. This feature aims to ensure that commands are only activated intentionally, improving the system's reliability for long-term use.

## Calibration
Calibration is straightforward and does not require any specific user interaction, thanks to the robust design which uses simple eye movement detection without the need for precise pupil tracking.


## Acknowledgments
- Prof. Dr. Tillmann Schwörer and Prof. Dr. Stephan Doerfel for their guidance.
- Prof. Dr. Florian Schatz for project oversight and support.

## Limitations
- Requires a well-lit environment for accurate detection.
- May need calibration for different lighting and facial features.

## Future Improvements
- Add support for more complex grids.
- Improve robustness in varying lighting conditions.
- Implement a calibration routine for different users.

## License
[MIT](https://choosealicense.com/licenses/mit/)
