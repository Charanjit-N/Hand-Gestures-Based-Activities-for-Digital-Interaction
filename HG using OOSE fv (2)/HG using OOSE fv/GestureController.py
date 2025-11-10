from abc import ABC, abstractmethod

class GestureController(ABC):
    _handlers = None  # Cache for control handlers

    @abstractmethod
    def process_gesture(self, fingers, landmarks, frame):
        """
        Abstract method to process gestures based on finger positions.
        """
        pass

    @staticmethod
    def get_control_handlers():
        """
        Return cached control handlers or create them if not already created.
        """
        if GestureController._handlers is None:
            from MouseControl import MouseControl
            from DocumentControl import DocumentControl
            from ZoomControl import ZoomControl  # Add the new ZoomControl
            GestureController._handlers = [MouseControl(), DocumentControl(), ZoomControl()]
        return GestureController._handlers

    @staticmethod
    def process_all_gestures(fingers, landmarks, frame):
        """
        Process gestures for all control handlers.
        """
        handlers = GestureController.get_control_handlers()
        for handler in handlers:
            handler.process_gesture(fingers, landmarks, frame)
