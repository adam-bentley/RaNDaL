# Weight groups for string (hammington distance)
string_groups = [["2", "Z"],
                 ["8", "B", "H"],
                 ["9", "5"],
                 ["O", "Q", "D", "0"],
                 ["G", "C"],
                 ["F", "P"],
                 ["D", "L"],
                 ["U", "V"]]

# Weight groups for ints
digit_groups = [
    ["Z", "2", ],
    ["B", "H", "8"],
    ["M", "O", "E", "Q", "D", "0"]
]


def weighted_hamming_distance(string1: str, string2: str) -> int:
    """
    Finds the difference between two strings by counting the new of substitutions
    Characters in the same group have a lesser cost
    :param string1: str First string
    :param string2: str Second string
    :return: int The distance score
    """
    # Start with a distance of zero, and count up
    distance = 0
    # Loop over the indices of the string
    length = len(string1)
    for i in range(length):
        # If they dont match
        if string1[i] != string2[i]:
            same_group = False
            # Find if there two differences are in the same weight class
            for group in string_groups:
                if string1[i] in group and string2[i] in group:
                    same_group = True
                    break
            # Increase the score by 0.5 if they're in the same group else, 1
            if same_group:
                distance += 0.5
            else:
                distance += 1
    # Return the final count of differences
    return distance


def correct_non_numeric(non_numeric: str) -> str:
    """
    Finds if a number if frequently miss predicted as a character
    :param non_numeric: The miss predicted character
    :return: str 0 or the number thats miss predict as this character
    """
    # Loop the groups
    for group in digit_groups:
        # If this character is in the group, return the number associated
        if non_numeric in group:
            return group[-1]

    return "0"
