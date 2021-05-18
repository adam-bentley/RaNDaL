import argparse
import os

from cv2.cv2 import VideoCapture, imread, imshow, waitKey, resize
from tensorflow.python.keras.models import load_model

from packages.models.racescreen import RaceScreen
from packages.models.racenet_connection import RacenetConnection


def testmode(model, rn):
    test_images_dir = "..//data//test_images//"

    # Entry list for the test images
    entry_list = ["L6", "L7", "L2", "L1", "L8", "L9", "L3", "L4", "L10", "L5", "L11", "L69", "L14", "L13", "L16", "L15",
                  "L19", "L17", "L18", "L20", "CB261", "CB216", "E189WKW", "888", "CB1040", "CB198", "CB79", "101",
                  "L22", "L24", "L25", "L21", "L27", "L23", "CC171", "L26", "L28", "L30", "L29", "L31", "L33", "L35",
                  "L34", "L39", "L36", "L41", "SSMA8608", "L40", "L44", "N1", "L45", "SPET167 ", "N2", "L51", "L50",
                  "L54", "L55", "L56", "L58", "L59", "L57", "L60", "NONE", "BS55", "53  ", "CB556   ", "PET706  ",
                  "L38", "L79", "L76", "L73", "L70", "L71", "L72", "L48", "L74", "L75", "L82", "C78", "N4 ", "L78",
                  "N5 ", "L80", "L81", "N3 ", "N7 ", "L47", "SPRO324 ", "SG1938  ", "N6  ", "212 ", "N19 ", "N16 ",
                  "N15 ", "N21 ", "N18 ", "N13 ", "N12 ", "N17 ", "N11 ", "JM3 ", "JS40", "JMA42   ", "JMA27   ",
                  "X743EKO ", "556", "34", "CB21", "CB701", "CB6", "SB1081", "P63HOV", "SB1080", "963", "SV04EKZ",
                  "SCOMP", "D69", "WB88", "STTG1", "DK04", "DK03", "DK56", "PET1089", "308", "PENNZOIL", "TAZ001",
                  "TAZ005", "L66", "L90", "N14", "L77", "N10", "L91", "SPRO700", "L99", "ST61NEY", "L105", "L146",
                  "Q144VWP", "L107", "P45", "N37", "L109", "S3DANF", "L49", "N38", "N36", "C45", "LLG", "N", "A79",
                  "ED03DAN", "N33", "N32", "N30", "N35", "B", "B555", "CB50", "2001", "1089", "1", "N54", "L46", "N31",
                  "L106", "L112", "C1", "C23", "SPET616", "G1", "CB57", "AA727", "121", "YG18ZGD", "L111", "MV04DVL"]

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

    capture = VideoCapture("http://192.168.0.11:8081/video.mjpg")
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
