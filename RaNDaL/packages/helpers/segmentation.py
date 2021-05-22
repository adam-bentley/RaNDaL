from numpy import sum, ndarray
from cv2 import hconcat


def calc_projection(image: ndarray, orientation: int = 0,
                    inverted: bool = False) -> ndarray:
    """
    Calculates the projection of text on an image
    :param image: The source image
    :param orientation: Set for vertical or horizontal projection
    :param inverted: True = Black text on a white background
    False = White text on black background
    :return: An array of projections
    """
    if not inverted:
        # For white text on black background
        # Convert black pixels to 0
        image[image == 0] = 0
        # Convert white pixels to 1
        image[image == 255] = 1
    else:
        # For black text on white background
        # Convert black pixels to 0
        image[image == 0] = 1
        # Convert white pixels to 1
        image[image == 255] = 0

    # 0 = vertical projection, 1 = horizontal projection
    projection = sum(image, axis=orientation)
    return projection


def split_merged_down_middle(text_area_frame: ndarray, character_start: int, character_end: int) -> list:
    """
    Takes a images that's too large to be a single character and divides it by the number of estimated characters
    :param text_area_frame: The text area containing the characters
    :param character_start: The start of the first merged character
    :param character_end: The end of the last merged character
    :return: list of now separated characters
    """
    # TODO clean
    # Estimate the number of characters
    estimated_characters = round((character_end - character_start) / 22)
    # The estimated length of each character
    interval = int(round(character_end - character_start) / estimated_characters)

    # List to store each character
    characters = []
    cursor = character_start

    while True:

        # If this is the final character
        if len(characters) == estimated_characters - 1:
            # Add the last character and break the loop
            character = (text_area_frame[0:text_area_frame.shape[0],
                         cursor:character_end])

            characters.append(character)
            break

        # Add the character from the cursor plus the length of the average character
        character = (text_area_frame[0:text_area_frame.shape[0],
                     cursor:cursor + interval])

        # Add the found character to the list
        characters.append(character)
        # Move the cursor to the start of the next character
        cursor += interval

    return characters


def split_characters(text_area_frame, ideal_projection=1):
    """
    Takes a image of multiple characters and segments them
    :param text_area_frame: Source image
    :param ideal_projection: Number of pixels
    in a column to be defined as an image
    :return: Array of character images
    """
    # List to store characters
    characters = []
    # Calc vertical projection
    vertical_projection = calc_projection(text_area_frame.copy())

    # Column cursor
    column = 0
    # Image width
    image_width = text_area_frame.shape[1]
    # Loop though image
    while column <= image_width - 1:
        # If column has part of character
        if vertical_projection[column] >= ideal_projection:
            # Store the location of the start of the character
            character_start = column
            # A second column cursor to find the end of the character
            next_column = column + 1
            # Loop second cursor until the character ends
            while vertical_projection[next_column] >= ideal_projection:
                next_column += 1
                # Check not on last column of image
                if next_column == image_width - 1:
                    break

            # Store the end character
            character_end = next_column
            # Catch the first cursor up
            column = next_column

            # Check that it has a width expect for a single character
            # If segmentation method 0, dont perform over segmentation
            if (character_end - character_start) > 30:
                characters.extend(split_merged_down_middle(
                    text_area_frame, character_start, character_end))
            else:
                # Add the character to the list
                characters.append(
                    text_area_frame[0:text_area_frame.shape[0],
                    character_start:character_end]
                )

        column += 1
    return characters


def fix_racenum_splitting(characters: list) -> list:
    """
    Reconstructs characters that have been split back together
    :param characters: List of split characters
    :return: List of reconstructed characters
    """

    if len(characters) == 0:
        return characters

    deletes = []
    i = 0
    # Characters normally only spilt once,
    # therefore if the first is split and so is the 3rd,
    # the 3rd belong to the second character
    # This loop simulates this process for the length of the characters
    # it merges the second character the first and adds the second to the delete pile
    while characters[i].shape[1] < 11:
        characters[i] = hconcat([characters[i], characters[i + 1]])
        deletes.append(i + 1)
        i += 2

        if i >= len(characters):
            break

    # Remove all the bad characters
    for index in deletes[::-1]:
        characters.pop(index)
    deletes = []

    i = -1
    # This does the same but from the end of the characters
    # it merges the first character the second and adds the first to the delete pile
    while characters[i].shape[1] < 11:
        characters[i - 1] = hconcat([characters[i - 1], characters[i]])
        deletes.append(i)
        i -= 2

        if i < 0:
            break

    # Remove all the bad characters
    for index in deletes[::-1]:
        characters.pop(index)
    deletes = []

    # Loops through each character, if the width is less then 11, its a split character
    # Find which side is smaller and merge them together
    for i in range(0, len(characters)-1):
        if characters[i].shape[1] < 11:
            left_width = characters[i - 1].shape[1]
            right_width = characters[i + 1].shape[1]

            if left_width > right_width:
                characters[i] = hconcat([characters[i], characters[i + 1]])
                deletes.append(i + 1)

            if left_width < right_width:
                characters[i - 1] = hconcat([characters[i - 1], characters[i]])
                deletes.append(i)

        i += 1

    for index in deletes[::-1]:
        characters.pop(index)

    return characters


def has_characters(text_field_frame):
    """
    Checks if text field has at least 1 character
    :param text_field_frame: The frame of the text field
    """
    # print(calc_projection(text_field_frame))
    if max(calc_projection(text_field_frame)) > 0:
        return True
    return False
