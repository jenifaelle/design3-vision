import cv2
import numpy as np


class Rectangle:
    def __init__(self, points):
        self._contour_points = points.tolist()

    def area(self):
        return cv2.contourArea(self.as_contour_points())

    def as_contour_points(self):
        return np.array(self._contour_points)

    def draw_in(self, image):
        cv2.drawContours(image, [self.as_contour_points()], -1, (0, 255, 0), 2)
