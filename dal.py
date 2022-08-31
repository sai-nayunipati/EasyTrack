"""
The data access layer (dal) is responsible for all database access.
"""

import mysql.connector


flagged_sections = []


def update_and_flag_sections_data(new_data):
    """
    Takes an array of JSON objects in the form {college, department, number, code, availability}
    and updates the "sections" table to reflect the new scrape data.

    If a section has went from unavailable to available, it is added to the "flagged sections" list.
    """
    db = mysql.connector.connect(
        user='root', password='', host='localhost', database='EasyTrack')
    cursor = db.cursor()

    sql = "SELECT * FROM sections"

    print(new_data)

    # Loop through every JSON in the list
    # If the section is in the table, update its fields.
    # If a section is not in the table, add it.
    # Delete any sections that are no longer in the list.


def get_invalid_tracks():
    """
    Returns an array of invalid tracks in the format {user_id, section_id}.
    """
    pass


def get_flagged_sections():
    """
    Returns an array of JSON objects representing sections that just became available.
    """
    pass


def get_email(user_id):
    """
    Returns the email address of the user with the given user_id.
    """
    pass


def get_section(section_id):
    """
    Returns the JSON object representing the section with the given section_id.
    """
    pass
