import numpy as np
from cv2 import medianBlur, cvtColor, COLOR_BGR2GRAY, THRESH_BINARY, threshold as th


def median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Applies a median filter to an image
    :param image: Source image
    :param kernel_size: Size of the kernel, default = 3
    :return: The processed image
    """
    if kernel_size > 3:
        image = medianBlur(image, kernel_size)
    return image


def threshold(image: np.ndarray, threshold_val: int = 110, max_val: int = 255) -> np.ndarray:
    """
    Thresholds an image
    :param image: Source image.
    :param threshold_val: Threshold value which is used to classify the pixel values. Default = 110.
    :param max_val: The value to be given if pixel value is more than threshold_val. Default = 255.
    :return: The processed image
    """
    ret, image = th(image, threshold_val, max_val, THRESH_BINARY)

    return image


def gray(image) -> np.ndarray:
    """
    Converts an image to gray scale
    :param image: Source image
    :return: Processed image
    """
    return cvtColor(image, COLOR_BGR2GRAY)