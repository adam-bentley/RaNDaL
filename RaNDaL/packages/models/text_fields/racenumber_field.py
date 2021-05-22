from numpy import ndarray
from tensorflow.python.keras import Sequential

from RaNDaL.packages.models.text_fields.text_field import TextArea
from RaNDaL.packages.helpers.segmentation import split_characters, fix_racenum_splitting
from RaNDaL.packages.helpers.postprocessing import weighted_hamming_distance


class RaceNumberField(TextArea):
    def __init__(self, frame: ndarray, model: Sequential, entry_list: list, inverted: bool = False):
        """
        Constructor for race number text area
        :param frame: Image of the text area
        :param model: CNN model for predictions
        :param entry_list: List of cars racenumbers to match the prediction too
        :param inverted: If its white text on a black background or black on white
        """
        # Call parent class
        super().__init__(frame, model, inverted=inverted)

        # Segmentate
        self.characters = split_characters(self.frame)

        # Post process
        if len(self.characters) != 0:
            self.characters = fix_racenum_splitting(self.characters)
            self.resize_characters()

            self.text = self.predict()

            self.post_process(entry_list)

    def post_process(self, entry_list: list):
        """
        Performs post processing
        :param entry_list: List of cars racenumbers to match the prediction too
        """
        # Post process
        # Check there is a entry list and a racenumber
        if len(entry_list) != 0 and len(self.text) != 0 and self.text not in entry_list:
            # Loop through each entry
            lowest_score = 10
            lowest_index = -1
            for i in range(0, len(entry_list)):
                # Check the entry is the same length of the text
                if len(self.text) == len(entry_list[i]):
                    # Get the hamming distance
                    score = weighted_hamming_distance(self.text, entry_list[i])
                    # If lower, update the lowest score and lowest index
                    if score < lowest_score:
                        lowest_score = score
                        lowest_index = i
            if lowest_index != -1:
                self.text = entry_list[lowest_index]
