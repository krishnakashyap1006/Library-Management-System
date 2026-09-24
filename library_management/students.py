from db import db_session


def add_student(student_name, student_branch, student_year):
    if not student_name.strip() or not student_branch.strip():
        raise ValueError("Student name aur branch required hain.")
    if student_year < 1:
        raise ValueError("Student year valid hona chahiye.")

    with db_session() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO students (student_name, student_branch, student_year)
            VALUES (%s, %s, %s)
            """,
            (student_name.strip(), student_branch.strip(), student_year),
        )
        student_id = cursor.lastrowid
        cursor.close()
        return student_id


def list_students():
    with db_session() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT student_id, student_name, student_branch, student_year
            FROM students
            ORDER BY student_id
            """
        )
        students = cursor.fetchall()
        cursor.close()
        return students
