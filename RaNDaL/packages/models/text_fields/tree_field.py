from numpy import ndarray
from tensorflow.python.keras import Sequential

from ...helpers.segmentation import split_characters
from .text_field import TextArea


class Tree(TextArea):
    def __init__(self, frame: ndarray, model: Sequential, inverted: bool = False):
        """
        Constrctor for a tree text area
        :param frame: The image containing the text
        :param model: CNN model for predictions
        :param inverted: If its white text on a black background or black on white
        """

        # Call parent
        super().__init__(frame, model, inverted=inverted)

        # Segmemtate
        self.characters = split_characters(self.frame)

        if len(self.characters) != 0:
            self.resize_characters()

            self.text = self.predict()

            if self.text[0] == "D":
                self.text = "D"
            elif self.text[0] == ".":
                # If the second letter is a 5
                # It could be a .5 Full, .5 X-OVER
                # or .5 Pro Tree
                if self.text[1] == "5":
                    if self.text[2] == "F":
                        self.text = ".5F"
                    elif self.text[2] == "X":
                        self.text = ".5X"
                    elif self.text[2] == "P":
                        self.text = ".5P"
                    else:
                        self.text = ""
                # It not .5 or 'D', it has to be a .4 Pro Tree
                elif self.text[1] == "4":
                    self.text = ".4P"