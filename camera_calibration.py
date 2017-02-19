import numpy as np
import cv2
import glob
import json

from camera.camera import Calibration
from camera.camera import CameraFactory

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
gray_image = None


def create_object_points():
    object_points = np.zeros((6 * 9, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
    return object_points


def load_calibration_images():
    return [cv2.imread(filename) for filename in glob.glob('data/images/calibration/*.jpg')]


def save_camera_model(camera_model):
    with open('./camera_model.json', 'w') as file:
        json.dump(camera_model.describe(), file, indent=4)


if __name__ == "__main__":
    camera_factory = CameraFactory()
    calibration = Calibration(camera_factory)

    calibration.add_target_points(create_object_points())

    images = load_calibration_images()
    for image in images:
        calibration.add_image(image)

    camera_model = calibration.do_calibration()

    save_camera_model(camera_model)