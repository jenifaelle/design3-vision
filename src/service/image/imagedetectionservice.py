import cv2
import numpy as np

from src.detector.worldelement.iworldelementdetector import IWorldElementDetector
from src.geometry.coordinate import Coordinate
from src.world.table import Table
from src.world.world import World
from world.robot import Robot


class ImageToWorldTranslator:
    def __init__(self, camera_model):
        self._camera_model = camera_model

    def create_world(self, table):
        table_corners = self._convert_table_image_points_to_world_coordinates(table)
        table_dimensions = self._get_table_dimension(table_corners)
        world_origin = table._rectangle.as_contour_points().tolist()[3]
        return World(table_dimensions['width'], table_dimensions['length'], world_origin[0], world_origin[1])

    def create_robot(self, robot):
        world_position = self._camera_model.compute_image_to_world_coordinates(robot._position[0],
                                                                               robot._position[1], 5.1)
        adjusted_position = self._camera_model.compute_world_to_image_coordinates(world_position[0],
                                                                                  world_position[1], 0)
        return adjusted_position

    def _convert_table_image_points_to_world_coordinates(self, table):
        table_corners = [self._camera_model.compute_image_to_world_coordinates(corner[0], corner[1], 0)
                         for corner in np.round(table._rectangle.as_contour_points()).astype('int').tolist()]
        return self._to_coordinates(table_corners)

    def _to_coordinates(self, points):
        return [Coordinate(point[0], point[1]) for point in points]

    def _get_table_dimension(self, table_corners):
        sides = self._get_table_sides_length(table_corners)
        return {
            "length": sides[0],
            "width": sides[3]
        }

    def _get_table_sides_length(self, table_corners):
        return sorted([table_corners[0].distance_from(table_corners[1]) * 4.7,
                       table_corners[1].distance_from(table_corners[2]) * 4.7,
                       table_corners[2].distance_from(table_corners[3]) * 4.7,
                       table_corners[3].distance_from(table_corners[0]) * 4.7])


class ImageDetectionService:
    def __init__(self, image_to_world_translator):
        self._detectors = []
        self._image_to_world_translator = image_to_world_translator

    def translate_image_to_world(self, image):
        world = None
        world_elements = self.detect_all_world_elements(image)
        for element in world_elements:
            element.draw_in(image)

        for image_element in world_elements:
            if isinstance(image_element, Table):
                world = self._image_to_world_translator.create_world(image_element)
            elif isinstance(image_element, Robot):
                robot = self._image_to_world_translator.create_robot(image_element)
                cv2.circle(image, tuple(robot), 2, (255, 0, 0), 2)
        return world

    def detect_all_world_elements(self, image):
        world_elements = []

        for detector in self._detectors:
            try:
                world_element = detector.detect(image)
                world_elements.append(world_element)
            except Exception as e:
                pass
                print("World initialisation failure: {}".format(type(e).__name__))

        return world_elements

    def register_detector(self, detector):
        if isinstance(detector, IWorldElementDetector):
            self._detectors.append(detector)

    def draw_world_elements_into(self, image, world_elements):
        for element in world_elements:
            element.draw_in(image)
