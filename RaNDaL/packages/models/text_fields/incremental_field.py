from cv2 import hconcat
from numpy import ndarray
from tensorflow.python.keras.engine.sequential import Sequential

from ...helpers.postprocessing import correct_non_numeric
from ...helpers.segmentation import split_characters
from .text_field import TextArea


class IncrementalField(TextArea):
    def __init__(self, frame: ndarray, model: Sequential, max_length: int = 7, inverted: bool = False):
        """
        Constructor for a incremental area of text
        R.T, 60' 330, 660 ET 660 Speed etc
        :param frame: The image containing the text
        :param model: CNN model for predictions
        :param max_length: Max length of the number
        :param inverted: If its white text on a black background or black on white
        """
        # Call the parent class
        super().__init__(frame, model, inverted=inverted)

        # Segmentate the characters
        self.characters = split_characters(self.frame)

        # If some characters were found
        if len(self.characters) != 0:
            # Resize and predict
            self.resize_characters()
            self.text = self.predict()
            self.max_length = max_length

            # Post process
            if len(self.text) != 0:
                self.post_process()

    def post_process(self):
        """
        Performs post processing
        """
        # If has extra characters
        if len(self.text) > self.max_length:
            self.fix_character_splitting()
        # Loop characters
        for character in self.text:
            # If is a-z
            if character.isalpha():
                # Replace with trending character or a 0
                self.text = self.text.replace(character, correct_non_numeric(character), 1)
                #pass

        if self.text == ".":
            self.text = "00.00"

        if len(self.text) > 1:
            if self.text[0] == "+" or self.text[0] == "-":
                if self.text[1] == ".":
                    self.text = self.text[0] + "0" + self.text[1:]

    def fix_character_splitting(self):
        """
        Fixes an issue where character would be split during segmentation
        This method merges them back together
        Its messy but it works
        """
        # TODO clean this
        # Find the index of the decimal
        try:
            dp_index = self.text.index(".")
        except ValueError:
            return

        try:
            # If the 1st character is too small, merge right
            if self.characters[0].shape[1] < 11 and len(self.characters) != self.max_length:
                # Merge and remove
                self.characters[0] = hconcat([self.characters[0], self.characters[1]])
                self.characters.pop(1)

                dp_index -= 1

                # If character 1 is a split and so is character 3, character 3 must belong to character 4
                if self.characters[1].shape[1] < 11:
                    self.characters[1] = hconcat([self.characters[1], self.characters[2]])
                    self.characters.pop(2)

                    dp_index -= 1
        except IndexError:
            pass

        try:
            # If the last character is too small, merge left
            if self.characters[-1].shape[1] < 11 and len(self.characters) != self.max_length:
                self.characters[-2] = hconcat([self.characters[-2], self.characters[-1]])
                self.characters.pop(-1)

                # If character -1 is a split and so is character -3, character -3 must belong to character -4
                if self.characters[-2].shape[1] < 11:
                    self.characters[-3] = hconcat([self.characters[-3], self.characters[-2]])
                    self.characters.pop(-2)
        except IndexError:
            pass

        try:
            # If the character before the decimal is too small, merge left
            if self.characters[dp_index - 1].shape[1] < 11 and len(self.characters) != self.max_length:
                self.characters[dp_index - 2] = hconcat([self.characters[dp_index - 2], self.characters[dp_index - 1]])
                self.characters.pop(dp_index - 1)
                dp_index -= 1

                # If the character before and 2 before the decimal is too small,
                # 2 before must belong to the character 3 before
                if self.characters[dp_index - 2].shape[1] < 11:
                    self.characters[dp_index - 3] = hconcat([self.characters[dp_index - 3], self.characters[dp_index - 2]])
                    self.characters.pop(dp_index - 2)
                    dp_index -= 1
        except IndexError:
            pass

        try:
            # If the character after the decimal is too small, merge right
            if self.characters[dp_index + 1].shape[1] < 11 and len(self.characters) != self.max_length:
                self.characters[dp_index + 1] = hconcat([self.characters[dp_index + 1], self.characters[dp_index + 2]])
                self.characters.pop(dp_index + 2)

                # If the character after and 2 after the decimal is too small,
                # 2 after must belong to the character 3 after
                if self.characters[dp_index + 2].shape[1] < 11:
                    self.characters[dp_index + 2] = hconcat([self.characters[dp_index + 2], self.characters[dp_index + 3]])
                    self.characters.pop(dp_index + 3)
        except IndexError:
            pass

        try:
            # If only 1 split between 2 numbers in the first half of the number, join the the smallest
            if self.characters[1].shape[1] < 11 and len(self.characters) != self.max_length:
                left = self.characters[0].shape[1]
                right = self.characters[2].shape[1]

                if right > left:
                    self.characters[0] = hconcat([self.characters[0], self.characters[1]])
                    self.characters.pop(1)
                else:
                    self.characters[2] = hconcat([self.characters[1], self.characters[2]])
                    self.characters.pop(1)
                    dp_index -= 1
        except:
            pass

        try:
            # If only 1 split between 2 numbers in the second half of the number, join the the smallest
            if self.characters[-2].shape[1] < 11 and len(self.characters) != self.max_length:
                left = self.characters[-3].shape[1]
                right = self.characters[-1].shape[1]

                if right > left:
                    self.characters[-3] = hconcat([self.characters[-3], self.characters[-2]])
                    self.characters.pop(-2)
                else:
                    self.characters[-1] = hconcat([self.characters[-2], self.characters[-1]])
                    self.characters.pop(-2)
        except:
            pass

        # Resize the characters and predict
        self.resize_characters()
        self.text = self.predict()