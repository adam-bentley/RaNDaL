import argparse
import csv
import os

from cv2.cv2 import VideoCapture, imread, imshow, waitKey, resize
from tensorflow.python.keras.models import load_model

from packages.models.racescreen import RaceScreen
from packages.models.racenet_connection import RacenetConnection


def testmode(model, rn):
    test_images_dir = "..//data//test_images//"

    # Entry list for the test images
    with open("..//data//test_images//entry_list.csv") as el:
        reader = csv.reader(el)
        entry_list = list(reader)[0]

    for image_dir in os.listdir(test_images_dir):
        image = imread(os.path.join(test_images_dir, image_dir))

        rs = RaceScreen(image, model, entry_list)
        rn.insert_predictions(rs.predictions_list())
        print(rs.to_table())

        imshow('Frame', resize(image, (700, 400)))
        print("Press any key to continue")
        waitKey(0)


def livemode(model, rn, load_entry_list):
    if load_entry_list:
        current_category = rn.select_current_category()
        entry_list = rn.select_entry_list(current_category)
    else:
        current_category = -1
        entry_list = []

    capture = VideoCapture("http://10.10.1.11:8081/video.mjpg")
    while capture.isOpened():
        ret, img = capture.read()
        rs = RaceScreen(img, model, entry_list)
        rn.insert_predictions(rs.predictions_list())
        print(rs.to_table())

        if load_entry_list:
            if current_category != rn.select_current_category():
                current_category = rn.select_current_category()
                entry_list = rn.select_current_category(current_category)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Set if the user wants to use the live stream or the test images
    parser.add_argument("--testmode", default=False, action='store_true',
                        help="Runs the OCR on the test images, instead of the live stream")
    parser.add_argument("--livemode", action='store_false',
                        help="Runs the OCR on the livestream (Default)")

    # Set if the user wants to use post-processing for race numbers
    parser.add_argument("--entrylist", default=False, action='store_true',
                        help="Use the database from the entry list (Default)")
    parser.add_argument("--no-entrylist", action='store_false',
                        help="Dont use the entry list from the database")

    args = parser.parse_args()

    # Load ML model
    model = load_model("files\\classifiers\\CNN.model")

    # Test the database connection
    rn = RacenetConnection()
    rn.test_connection()

    if args.testmode:
        testmode(model, rn)
    else:
        livemode(model, rn, args.entrylist)
