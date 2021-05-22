from numpy import ndarray
from tensorflow.python.keras import Sequential

from RaNDaL.packages.models.text_fields.text_field import TextArea
from RaNDaL.packages.helpers.segmentation import has_characters, split_characters


class BoolField(TextArea):
    def __init__(self, frame: ndarray, active_text: str, inverted: bool = True):
        """
        Constructor for bool text field (On or off)
        i.e Staged, cell out, tower ready etc
        :param frame: Source image
        :param inverted: If its white text on a black background or black on white
        """
        # Call parent
        super().__init__(frame, None, inverted=inverted)

        self.active = has_characters(self.frame.copy())

        if self.active:
            self.text = active_text
