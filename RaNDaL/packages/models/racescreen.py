from numpy import ndarray
from tensorflow.python.keras import Sequential
from terminaltables import AsciiTable

from ..helpers.preprocessing import median_filter, gray, threshold
from ..models.text_fields.tree_field import Tree
from ..models.text_fields.incremental_field import IncrementalArea
from ..models.text_fields.racenumber_field import RaceNumberArea


class RaceScreen:
    def __init__(self, image: ndarray, model: Sequential, entry_list: list = []):
        """
        Constructor for the race screen
        :type image: Image of the race computer screen
        """
        # Preprocess image
        image = median_filter(image, kernel_size=1)
        image = gray(image)
        image = threshold(image)

        # Tree
        self.tree = Tree(image[921:948, 575:860], model, inverted=True)

        # Left lane values
        self.left_race_num = RaceNumberArea(image[175:202, 270:550], model, entry_list, inverted=True)
        self.left_dial_in = IncrementalArea(image[175:202, 720:910], model, max_length=5, inverted=True)

        self.left_reaction = IncrementalArea(image[217: 243, 580:875], model, max_length=8)
        self.left_60_et = IncrementalArea(image[258: 284, 580:875], model)
        self.left_330_et = IncrementalArea(image[299: 326, 580:875], model)
        self.left_660_et = IncrementalArea(image[341: 367, 580:875], model)
        self.left_660_speed = IncrementalArea(image[383: 409, 580:875], model, max_length=6)
        self.left_1000_et = IncrementalArea(image[424: 450, 580:875], model)
        self.left_1000_speed = IncrementalArea(image[465: 492, 580:875], model, max_length=6)
        self.left_1320_et = IncrementalArea(image[548: 575, 580:875], model)
        self.left_1320_speed = IncrementalArea(image[590: 616, 580:875], model, max_length=6)

        self.left_next_race_num = RaceNumberArea(image[756:781, 240:520], model, entry_list)
        self.left_next_dial_in = IncrementalArea(image[756:781, 700:900], model, max_length=5)

        # Right lane
        self.right_race_num = RaceNumberArea(image[175:202, 1230:1510], model, entry_list, inverted=True)
        self.right_dial_in = IncrementalArea(image[175:202, 1700:1870], model, max_length=5, inverted=True)

        self.right_reaction = IncrementalArea(image[217: 243, 1500:1850], model, max_length=8)
        self.right_60_et = IncrementalArea(image[258: 284, 1500:1850], model)
        self.right_330_et = IncrementalArea(image[299: 326, 1500:1850], model)
        self.right_660_et = IncrementalArea(image[341: 367, 1500:1850], model)
        self.right_660_speed = IncrementalArea(image[383: 409, 1500:1850], model, max_length=6)
        self.right_1000_et = IncrementalArea(image[424: 450, 1500:1850], model)
        self.right_1000_speed = IncrementalArea(image[465: 492, 1500:1850], model, max_length=6)
        self.right_1320_et = IncrementalArea(image[548: 575, 1500:1850], model)
        self.right_1320_speed = IncrementalArea(image[590: 616, 1500:1850], model, max_length=6)

        self.right_next_race_num = RaceNumberArea(image[756:781, 1250:1500], model, entry_list)
        self.right_next_dial_in = IncrementalArea(image[756:781, 1700:1870], model, max_length=5)

    def to_table(self) -> AsciiTable:
        """
        Get all the predictions in a ascii table
        """
        # Output data
        data = [
            ['Left Lane', '', 'Right Lane'],
            # ['', self.tower_ready.text, ''],
            [self.left_race_num.text, 'VS', self.right_race_num.text],
            [self.left_dial_in.text, 'Dial-in', self.right_dial_in.text],
            ['', 'Staged', ''],
            [self.left_reaction.text, 'RT', self.right_reaction.text],
            [self.left_60_et.text, '60 et.text', self.right_60_et.text],
            [self.left_330_et.text, '330 et.text', self.right_330_et.text],
            [self.left_660_et.text, '660 et.text', self.right_660_et.text],
            [self.left_660_speed.text, '660 SP', self.right_660_speed.text],
            [self.left_1000_et.text, '1000 et.text', self.right_1000_et.text],
            [self.left_1000_speed.text, '1000 SP', self.right_1000_speed.text],
            [self.left_1320_et.text, '1320 ET', self.right_1320_et.text],
            [self.left_1320_speed.text, '1320 ET', self.right_1320_speed.text],
            [self.left_next_race_num.text, 'VS', self.right_next_race_num.text],
            [self.left_next_dial_in.text, 'Dial-in', self.right_next_dial_in.text],
            ['', self.tree.text, '']
        ]

        table = AsciiTable(data)
        table.justify_columns[0] = 'left'
        table.justify_columns[1] = 'center'
        table.justify_columns[2] = 'right'

        return table.table

    def predictions_list(self) -> list:
        """
        Get all the predicts as a list
        """
        # TODO handle these
        return list((
            # self.tower_ready.text,
            self.tree.text,
            self.left_race_num.text,
            self.left_dial_in.text,
            self.left_reaction.text,
            self.left_60_et.text,
            self.left_330_et.text,
            self.left_660_et.text,
            self.left_660_speed.text,
            self.left_1000_et.text,
            self.left_1000_speed.text,
            self.left_1320_et.text,
            self.left_1320_speed.text,
            self.left_next_race_num.text,
            self.left_next_dial_in.text,

            self.right_race_num.text,
            self.right_dial_in.text,
            self.right_reaction.text,
            self.right_60_et.text,
            self.right_330_et.text,
            self.right_660_et.text,
            self.right_660_speed.text,
            self.right_1000_et.text,
            self.right_1000_speed.text,
            self.right_1320_et.text,
            self.right_1320_speed.text,
            self.right_next_race_num.text,
            self.right_next_dial_in.text))
