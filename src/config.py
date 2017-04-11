import numpy as np

BASESTATION_WEBSOCKET_URL = 'ws://localhost:3000'
CAMERA_MODELS_FILE_PATH = '../data/camera_models/camera_models.json'
TABLE_CAMERA_MODEL_ID = 2
TEST_IMAGE_DIRECTORY_PATH = '../data/images/full_scene/*.jpg'
CAMERA_ID = 1
CAP_WIDTH = 1280
CAP_HEIGHT = 800

# HSV COLOR
LOWER_GREEN_HSV = np.array([45, 45, 100])
UPPER_GREEN_HSV = np.array([80, 255, 255])

LOWER_FUCHSIA_HSV = np.array([148, 5, 100])
HIGHER_FUCHSIA_HSV = np.array([180, 255, 255])

LOWER_BACKGROUND = np.array([0, 0, 50])
UPPER_BACKGROUND = np.array([180, 50, 255])

LOWER_FIGURE_HSV = np.array([30, 80, 75])
UPPER_FIGURE_HSV = np.array([80, 255, 255])

# ROBOT MARKERS SPECIFICATIONS
NUMBER_OF_MARKERS = 3
TARGET_MIN_DISTANCE = 12
TARGET_MIN_RADIUS = 5
TARGET_MAX_RADIUS = 30
MIN_TABLE_AREA = 70000
TARGET_SIDE_LENGTH = 44  # in mm

# ROBOT SPECIFICATIONS
ROBOT_HEIGHT_IN_MM = 270
ROBOT_HEIGHT_IN_TARGET_UNIT = ROBOT_HEIGHT_IN_MM / TARGET_SIDE_LENGTH
OBSTACLE_HEIGHT_IN_TARGET_UNIT = 10
