from numpy import ndarray
from tensorflow.python.keras import Sequential
from terminaltables import AsciiTable
import json

from RaNDaL.packages.helpers.preprocessing import median_filter, gray, threshold
from RaNDaL.packages.helpers.segmentation import split_characters
from RaNDaL.packages.models.text_fields.tree_field import Tree
from RaNDaL.packages.models.text_fields.incremental_field import IncrementalField
from RaNDaL.packages.models.text_fields.racenumber_field import RaceNumberField
from RaNDaL.packages.models.text_fields.bool_field import BoolField


class RaceScreen:
    def __init__(self, category_name, image: ndarray, model: Sequential, entry_list: list = []):
        """
        Constructor for the race screen
        :type image: Image of the race computer screen
        """
        # Preprocess image
        image = median_filter(image, kernel_size=1)
        image = gray(image)
        image = threshold(image)

        # Check its a valid racescreen
        if len(split_characters(image[0:45, 1750:1950])) == 0:
            self.valid = False
            return

        self.valid = True
        self.category_name = category_name

        # Tree
        self.tree = Tree(image[921:948, 575:860], model, inverted=True)
        self.cell_warning = BoolField(image[176:200, 983:1002], "CELL WARNING", inverted=False)

        # Left lane values
        self.left_race_num = RaceNumberField(image[175:202, 270:550], model, entry_list, inverted=True)
        self.left_dial_in = IncrementalField(image[175:202, 720:910], model, max_length=5, inverted=True)
        self.left_staged = BoolField(image[91:120, 142:285], "STAGED")

        self.left_reaction = IncrementalField(image[217: 243, 580:875], model, max_length=8)
        self.left_60_et = IncrementalField(image[258: 284, 580:875], model)
        self.left_330_et = IncrementalField(image[299: 326, 580:875], model)
        self.left_660_et = IncrementalField(image[341: 367, 580:875], model)
        self.left_660_speed = IncrementalField(image[383: 409, 580:875], model, max_length=6)
        self.left_1000_et = IncrementalField(image[424: 450, 580:875], model)
        self.left_1000_speed = IncrementalField(image[465: 492, 580:875], model, max_length=6)
        self.left_1320_et = IncrementalField(image[548: 575, 580:875], model)
        self.left_1320_speed = IncrementalField(image[590: 616, 580:875], model, max_length=6)

        self.left_next_race_num = RaceNumberField(image[756:781, 240:520], model, entry_list)
        self.left_next_dial_in = IncrementalField(image[756:781, 700:900], model, max_length=5)

        # Right lane
        self.right_race_num = RaceNumberField(image[175:202, 1230:1510], model, entry_list, inverted=True)
        self.right_dial_in = IncrementalField(image[175:202, 1700:1870], model, max_length=5, inverted=True)
        self.right_staged = BoolField(image[92:119, 1702:1845], "STAGED")

        self.right_reaction = IncrementalField(image[217: 243, 1500:1850], model, max_length=8)
        self.right_60_et = IncrementalField(image[258: 284, 1500:1850], model)
        self.right_330_et = IncrementalField(image[299: 326, 1500:1850], model)
        self.right_660_et = IncrementalField(image[341: 367, 1500:1850], model)
        self.right_660_speed = IncrementalField(image[383: 409, 1500:1850], model, max_length=6)
        self.right_1000_et = IncrementalField(image[424: 450, 1500:1850], model)
        self.right_1000_speed = IncrementalField(image[465: 492, 1500:1850], model, max_length=6)
        self.right_1320_et = IncrementalField(image[548: 575, 1500:1850], model)
        self.right_1320_speed = IncrementalField(image[590: 616, 1500:1850], model, max_length=6)

        self.right_next_race_num = RaceNumberField(image[756:781, 1250:1500], model, entry_list)
        self.right_next_dial_in = IncrementalField(image[756:781, 1700:1870], model, max_length=5)

    def to_table(self) -> AsciiTable:
        """
        Get all the predictions in a ascii table
        """
        # Output data
        data = [
            ['Left Lane', self.category_name, 'Right Lane'],
            # ['', self.tower_ready.text, ''],
            [self.left_race_num.text, 'VS', self.right_race_num.text],
            [self.left_dial_in.text, 'Dial-in', self.right_dial_in.text],
            [self.left_staged.text, 'Staged', self.right_staged.text],
            [self.left_reaction.text, 'RT', self.right_reaction.text],
            [self.left_60_et.text, '60 ET', self.right_60_et.text],
            [self.left_330_et.text, '330 ET', self.right_330_et.text],
            [self.left_660_et.text, '660 ET', self.right_660_et.text],
            [self.left_660_speed.text, '660 SP', self.right_660_speed.text],
            [self.left_1000_et.text, '1000 ET', self.right_1000_et.text],
            [self.left_1000_speed.text, '1000 SP', self.right_1000_speed.text],
            [self.left_1320_et.text, '1320 ET', self.right_1320_et.text],
            [self.left_1320_speed.text, '1320 ET', self.right_1320_speed.text],
            [self.left_next_race_num.text, 'VS', self.right_next_race_num.text],
            [self.left_next_dial_in.text, 'Dial-in', self.right_next_dial_in.text],
            ['', self.tree.text, ''],
            ['', self.cell_warning.text, ''],
        ]

        table = AsciiTable(data)
        table.justify_columns[0] = 'left'
        table.justify_columns[1] = 'center'
        table.justify_columns[2] = 'right'

        return table.table

    def to_tuple(self) -> tuple:
        query = ["2016-06-22 19:10:25-07",
                 self.tree.text,
                 '',
                 str(self.cell_warning.active),
                 '',
                 self.left_race_num.text,
                 str(self.left_staged.active),
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
                 str(self.right_staged.active),
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
                 self.right_next_dial_in.text, ]

        for i in range(0, len(query) - 1):
            if query[i] == '':
                query[i] = None

        return tuple(query)
