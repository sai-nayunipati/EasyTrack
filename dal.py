"""
The data access layer (dal) is responsible for all database access.
"""

import code
import mysql.connector


flagged_sections = []


def update_courses(courses):
    """
    Inserts new courses into the "courses" table.
    Ignores any courses that are already in the table.
    Takes an array of JSON objects in the form {college, department, number}.

    Help:
    https://stackoverflow.com/questions/3164505/mysql-insert-record-if-not-exists-in-table
    """
    db = mysql.connector.connect(
        user='root', password='', host='localhost', database='easytrack_db')
    cursor = db.cursor()

    for c in courses:
        sql = f"""
            INSERT INTO courses (college, department, number)
            SELECT '{c['college']}', '{c['department']}', '{c['number']}'
            WHERE NOT EXISTS
            (SELECT * FROM courses WHERE college = '{c['college']}'
            AND department = '{c['department']}' AND number = '{c['number']}')
            """
        cursor.execute(sql)

    db.commit()
    db.close()


def update_sections(sections):
    """
    Inserts new sections into the "courses" table.
    Ignores any sections that are already in the table.
    Takes an array of JSON objects in the form {college, department, number, code, is_available}.

    If a section has went from unavailable to available, it is added to the "flagged sections" list.

    Help:
    https://stackoverflow.com/questions/3164505/mysql-insert-record-if-not-exists-in-table
    """
    db = mysql.connector.connect(
        user='root', password='', host='localhost', database='easytrack_db')
    cursor = db.cursor()

    # Insert new sections
    for s in sections:
        # Get the course_id of the course that this section belongs to.
        sql = f"""
            SELECT course_id FROM courses
            WHERE college = '{s['college']}' AND department = '{s['department']}'
            AND number = '{s['number']}'
            """
        cursor.execute(sql)
        course_id = cursor.fetchone()[0]

        # Insert the section if it doesn't already exist
        sql = f"""
            INSERT INTO sections (course_id, code, is_available)
            SELECT '{course_id}', '{s['code']}', '0'
            WHERE NOT EXISTS
            (SELECT * FROM sections WHERE course_id = '{course_id}'
            AND code = '{s['code']}')
            """
        cursor.execute(sql)

    # Mark all sections as unavailable.
    sql = "UPDATE sections SET is_available = '0'"
    cursor.execute(sql)

    # Enumerate through all sections and mark them as available if they are available.
    for s in sections:
        availability_to_int = 1 if s['is_available'] else 0
        # Need to do

    db.commit()
    db.close()


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
