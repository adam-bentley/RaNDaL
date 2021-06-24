from psycopg2 import DatabaseError, connect

from RaNDaL.packages.helpers.racenet_connection_config import config
from RaNDaL.packages.models.racescreen import RaceScreen


class RacenetConnection:
    def __init__(self) -> None:
        """
        Sets up ready to connect the racenet db
        """
        self.conn = None
        self.paramas = config()

    def open_connection(self):
        """
        Opens a connection to racenet
        """
        try:
            self.conn = connect(**self.paramas)
        except (Exception, DatabaseError) as error:
            print("Error opening connection:")
            print(error)

    def close_connection(self):
        """
        Closes a connection with racenet
        """
        if self.conn is not None:
            self.conn.close()

    def test_connection(self):
        """
        Tries to connect to racenet db and print DB version
        """
        print("Attempting to connect to Racenet DB")
        try:
            # Open connection
            self.open_connection()
            cur = self.conn.cursor()

            cur.execute("Select VERSION()")
            db_version = cur.fetchone()

            cur.close()

            print("Successfully connected to Racenet DB")
            print("DB Version:", db_version)

        except (Exception, DatabaseError) as error:
            print("Error in connecting to Racenet DB")
            print(error)

        finally:
            self.close_connection()

    def select_current_category_id(self) -> int:
        """
        Get the current selected category from the DB
        :return: int Current category id
        """
        current_category = -1
        try:
            self.open_connection()
            cur = self.conn.cursor()
            cur.execute('SELECT rn_config."CurrentCategory" from rn_config')

            current_category = (cur.fetchone())[0]
            cur.close
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            self.close_connection()

        return current_category

    def select_current_category_name(self, current_category_id):
        """
        Get current category name
        :param current_category_id:Id of the category
        :return: The category name
        """
        current_name = ""
        try:
            self.open_connection()
            cur = self.conn.cursor()
            cur.execute('SELECT name from rn_categ where id = ' + str(current_category_id))
            current_name = (cur.fetchone())[0].strip()
            cur.close()
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            self.close_connection()

        return current_name

    def select_entry_list(self, current_category: int) -> list:
        """
        Gets a list of racenumbers for the selected category for postprocessing
        :rtype: list (str) of racenumbers
        """
        racenumbers = []
        try:
            self.open_connection()
            cur = self.conn.cursor()
            cur.execute("SELECT racenum " +
                        "FROM rn_racers " +
                        "WHERE category = {}".format(current_category))

            row = cur.fetchone()

            while row is not None:
                racenumbers.append(str(row[0].rstrip()))
                row = cur.fetchone()

            cur.close
        except (Exception, DatabaseError) as error:
            print(error)
        finally:
            self.close_connection()
        return racenumbers

    def insert_predictions(self, rs: RaceScreen):
        """
		Clear the cnn_prediction table and
        Insert new predictions into the database
        :param predictions: Race screen tuple with all the parameters
        """
        try:
            self.open_connection()
            cur = self.conn.cursor()

            cur.execute("DELETE FROM cnn_currentpair")

            sql = """
                INSERT INTO public.cnn_currentpair(
                datetime, towerready, cellwarning, runactive, leftracenum, leftstaged, leftindex, leftreaction, leftet60, 
                leftet330, leftet660, leftspeed660, leftet1000, leftspeed1000, leftet1320, leftspeed1320, leftnextracenum, 
                leftnextindex, rightracenum, rightstaged, rightindex, rightreaction, rightet60, rightet330, rightet660, 
                rightspeed660, rightet1000, rightspeed1000, rightet1320, rightspeed1320, rightnextracenum, rightnextindex, 
                tree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
	        """

            # cur.execute(sql, (None, None, None, None, None,
            #                   None, None, None, None,
            #                   None, None, None,
            #                   None, None, None,
            #                   None, None, None,
            #                   None, None, None, None,
            #                   None, None, None,
            #                   None, None, None,
            #                   None, None, None,
            #                   None, None))

            cur.execute(sql, (None, None, rs.cell_warning.active, None, rs.left_race_num.get_text()[:8],
                              rs.left_staged.active, rs.left_dial_in.get_text(), rs.left_reaction.get_text(),
                              rs.left_60_et.get_text(), rs.left_330_et.get_text(), rs.left_660_et.get_text(),
                              rs.left_660_speed.get_text(), rs.left_1000_et.get_text(), rs.left_1000_speed.get_text(),
                              rs.left_1320_et.get_text(), rs.left_1320_speed.get_text(),
                              rs.left_next_race_num.get_text(), rs.left_next_dial_in.get_text(),
                              rs.right_race_num.get_text()[:8],
                              rs.right_staged.active, rs.right_dial_in.get_text(), rs.right_reaction.get_text(),
                              rs.right_60_et.get_text(), rs.right_330_et.get_text(), rs.right_660_et.get_text(),
                              rs.right_660_speed.get_text(), rs.right_1000_et.get_text(), rs.right_1000_speed.get_text(),
                              rs.right_1320_et.get_text(), rs.right_1320_speed.get_text(),
                              rs.right_next_race_num.get_text(), rs.right_next_dial_in.get_text(), rs.tree.get_text()))

            self.conn.commit()
            cur.close()
            self.close_connection()
        except (Exception, DatabaseError) as e:
            print(e)


def convert_list(prediction_list: list) -> list:
    """
    Converts the list of predictions to SQL format
    :param prediction_list: List of python predictions
    :return: List of sql converted predictions
    """
    string = ""

    for x in prediction_list:
        if x != "":
            string += "'" + x + "',"
        else:
            string += "NULL,"

    return string[:-1]
