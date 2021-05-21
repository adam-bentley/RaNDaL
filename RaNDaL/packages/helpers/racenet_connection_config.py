from configparser import ConfigParser


def config(
        filename: str = "files//db_configs//racenetdb.ini",
        section: str = "Postgres") -> dict:
    """
    Gets the database info from the .ini file
    :param filename: Location of the .ini file, this needs to be its full path
    :param section: Section to find
    :return: dict of database paramas
    """
    # Read the file
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    # Find the section
    if parser.has_section(section):
        params = parser.items(section)
        # Store the paramas
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
