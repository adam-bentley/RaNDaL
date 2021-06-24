import string

from cv2.cv2 import bitwise_not, resize
from numpy import argmax, ndarray
from matplotlib.pyplot import imshow, show, subplots
from tensorflow.python.keras import Sequential


class TextArea:
    def __init__(self, frame: ndarray, model: Sequential, inverted: bool = False):
        """
        Constructor for a text area
        Override by racenumber and incremental
        :param frame: Image of the text area
        :param model: CNN model for predictions
        :param inverted: If its white text on a black background or black on white
        """

        # If inverted, invert the image
        if inverted:
            frame = bitwise_not(frame)

        # Set base values
        self.frame = frame
        self.characters = None
        self.characters_resized = None
        self.cnn = model
        self.text = ""

    def resize_characters(self):
        """
        Takes the characters from self.characters and resizes them to the expect sized for the model (26, 22)
        """
        self.characters_resized = [resize(x, (26, 22)) for x in self.characters]

    def predict(self) -> list:
        """
        Predicts and decodes the value for each of the characters
        :rtype: list of decoded predictions
        """
        if len(self.characters_resized) > 0:
            predictions = []

            for character in self.characters_resized:
                result = self.cnn([character.reshape(-1, 26, 22, 1)])
                predictions.append(argmax(result, axis=1)[0])

            return decode_labels(predictions)

    def plot_characters(self):
        """
        Displays a plot of all the characters
        """
        if len(self.characters) > 1:
            fig, ax = subplots(1, len(self.characters))
            for x in range(0, len(self.characters)):
                ax[x].imshow(self.characters[x], cmap='gray')
            show()
        if len(self.characters) == 1:
            imshow(self.characters[0], cmap='gray')
            show()

    def get_text(self) -> str:
        if self.text == '':
            return None
        return self.text


def decode_labels(encoded_labels: list) -> str:
    """
    Decodes predictions to their string equivalent
    :param encoded_labels: List of encoded predictions
    :return: Str of decoded predictions
    """
    labels = string.digits + string.ascii_uppercase + "." + "+" + "-" + "?"
    text = ""

    for x in encoded_labels:
        text += labels[x]
    return text
