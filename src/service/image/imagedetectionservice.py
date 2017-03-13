import glob
import cv2
import numpy as np

from src.detector.worldelement.iworldelementdetector import IWorldElementDetector
from service.image.detectonceproxy import DetectOnceProxy
from src.detector.worldelement.robotdetector import RobotDetector
from src.geometry.coordinate import Coordinate
from src.infrastructure.camera import JSONCameraModelRepository
from src.detector.worldelement.drawingareadetector import DrawingAreaDetector
from src.detector.worldelement.shapefactory import ShapeFactory
from src.detector.worldelement.tabledetector import TableDetector
from src.world.table import Table
from src.world.world import World


class ImageToWorldTranslator:
    def __init__(self, camera_model):
        self._camera_model = camera_model

    def create_world(self, table):
        table_corners = self._convert_table_image_points_to_world_coordinates(table)
        table_dimensions = self._get_table_dimension(table_corners)
        return World(table_dimensions['width'], table_dimensions['length'])

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
        return world

    def detect_all_world_elements(self, image):
        world_elements = []

        for detector in self._detectors:
            try:
                world_element = detector.detect(image)
                world_elements.append(world_element)
            except Exception as e:
                print("World initialisation failure: {}".format(type(e).__name__))

        return world_elements

    def register_detector(self, detector):
        if isinstance(detector, IWorldElementDetector):
            self._detectors.append(detector)

    def draw_world_elements_into(self, image, world_elements):
        for element in world_elements:
            element.draw_in(image)


if __name__ == '__main__':
    camera_model_repository = JSONCameraModelRepository('../../data/camera_models/camera_models.json')
    camera_model = camera_model_repository.get_camera_model_by_id(0)
    image_to_world_translator = ImageToWorldTranslator(camera_model)

    shape_factory = ShapeFactory()

    table_detector = TableDetector(shape_factory)
    drawing_area_detector = DrawingAreaDetector(shape_factory)

    table_detector_proxy = DetectOnceProxy(table_detector)
    drawing_area_detector_proxy = DetectOnceProxy(drawing_area_detector)

    robot_detector = RobotDetector(shape_factory)

    detection_service = ImageDetectionService(image_to_world_translator)
    detection_service.register_detector(drawing_area_detector_proxy)
    detection_service.register_detector(table_detector_proxy)
    detection_service.register_detector(robot_detector)

    for filename in glob.glob('../../data/images/full_scene/*.jpg'):
        image = cv2.imread(filename)
        image = camera_model.undistort_image(image)

        world = detection_service.translate_image_to_world(image)

        cv2.imshow('World Image', image)
        cv2.waitKey()
