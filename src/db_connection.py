import sqlite3
from datetime import datetime 

connection = sqlite3.connect('../database/shared_database.db', check_same_thread=False)
cursor = connection.cursor()

def change_first_name(first_name, matriculation_number):
    print(f'LOG change_first_name: Change the first name to {first_name} for {matriculation_number}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return "Student not found"
        cursor.execute('UPDATE students SET first_name = ? WHERE matriculation_number = ?', (first_name, matriculation_number))
        connection.commit()
        
        return f"Your first name changed to {first_name} successfully"
    except Exception as e:
        return f"An error occurred while changing the first name: {str(e)}"

def change_last_name(last_name, matriculation_number):
    print(f'LOG change_last_name: Change the last name to {last_name} for {matriculation_number}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return "Student not found"
        cursor.execute('UPDATE students SET last_name = ? WHERE matriculation_number = ?', (last_name, matriculation_number))
        connection.commit()

        return f"Your last name changed to {last_name} successfully"
    except Exception as e:
        return f"An error occurred while changing the last name: {str(e)}"

def change_address(address, city, post_code, matriculation_number):
    print(f'LOG change_address: Change address {address}, city {city}, post_code {post_code}, for {matriculation_number}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return "Student not found"
        student_id = student_id_result[0]
        cursor.execute('UPDATE student_address SET address = ?, city = ?, post_code = ? WHERE student_id = ?', 
                    (address, city, post_code, student_id))
        connection.commit()

        return f"Your address changed to {address}, {city} {post_code} successfully"
    except Exception as e:
        return f"An error occurred while changing address: {str(e)}"
    
def register_exam(course_name, matriculation_number):
    print(f'LOG register_exam: Register {matriculation_number} for exam {course_name}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return f"Student with matriculation number {matriculation_number} is not found"
        student_id = student_id_result[0]

        cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
        course_id_result = cursor.fetchone()
        if not course_id_result:
            return f"Course with name {course_name} is not found"
        course_id = course_id_result[0]

        cursor.execute('SELECT id, time FROM exams WHERE course_id = ?', (course_id,))
        exam_result = cursor.fetchone()
        if not exam_result:
            return f"{course_name} exam is not found"
        exam_id, exam_time = exam_result

        exam_datetime = datetime.strptime(exam_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        if exam_datetime < current_time:
            return f"{course_name} exam already completed on {exam_time}"

        cursor.execute('SELECT id FROM student_exams WHERE student_id = ? AND exam_id = ?', (student_id, exam_id))
        student_exam_result = cursor.fetchone()
        if student_exam_result:
            return f"Student with matriculation number {matriculation_number} has already exam {course_name} on {exam_time}"        

        cursor.execute('INSERT INTO student_exams (student_id, exam_id) VALUES (?, ?)', (student_id, exam_id))
        connection.commit()

        return f"You registered for {course_name} exam successfully"
    except Exception as e:
        return f"An error occurred while registering for the exam: {str(e)}"


def deregister_exam(course_name, matriculation_number):
    print(f'LOG deregister_exam: Deregister {matriculation_number} from exam {course_name}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return f"Student with matriculation number {matriculation_number} is not found"
        student_id = student_id_result[0]

        cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return f"Course with name {course_name} is not found"
        course_id = student_id_result[0]

        cursor.execute('SELECT id, time FROM exams WHERE course_id = ?', (course_id,))
        exam_id_result = cursor.fetchone()
        if not exam_id_result:
            return f"{course_name} exam is not found"
        exam_id, exam_time = exam_id_result

        cursor.execute('SELECT id FROM student_exams WHERE student_id = ? AND exam_id = ?', (student_id, exam_id))
        student_exam_result = cursor.fetchone()
        if not student_exam_result:
            return f"Student with matriculation number {matriculation_number} does not have exam {course_name}"

        exam_datetime = datetime.strptime(exam_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        if exam_datetime < current_time:
            return f"{course_name} exam already completed on {exam_time}"

        cursor.execute('DELETE FROM student_exams where student_id = ? and exam_id = ?', (student_id, exam_id))
        connection.commit()

        return f"You deregistered from {course_name} exam successfully"
    except Exception as e:
        return f"An error occurred while dereginstering from the exam: {str(e)}"

def query_exam_status(course_name, matriculation_number):
    print(f'LOG query_exam_status: Query exam status {matriculation_number} for exam {course_name}')
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return f"Student with matriculation number {matriculation_number} is not found"
        student_id = student_id_result[0]

        cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
        course_id_result = cursor.fetchone()
        if not course_id_result:
            return f"Course with name {course_name} is not found"
        course_id = course_id_result[0]

        cursor.execute('SELECT id, time FROM exams WHERE course_id = ?', (course_id,))
        exam_result = cursor.fetchone()
        if not exam_result:
            return f"{course_name} exam is not found"
        exam_id, exam_time = exam_result

        cursor.execute('SELECT * FROM student_exams WHERE exam_id = ? AND student_id = ?', (exam_id, student_id))
        student_exam_result = cursor.fetchone()
        if not student_exam_result:
            return f"Your status for {course_name} is Not Registered"
        
        exam_datetime = datetime.strptime(exam_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        if exam_datetime > current_time:
            return f"Your status for {course_name} is Registered"
        else:
            return f"Examination for {course_name} already completed"
    except Exception as e:
        return f"An error occurred while quering the exam status: {str(e)}"

def query_exam_grade(course_name, matriculation_number):
    print(f'LOG query_exam_grade: Query grade {matriculation_number} for exam {course_name}')
    
    try:
        cursor.execute('SELECT id FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_id_result = cursor.fetchone()
        if not student_id_result:
            return f"Student with matriculation number {matriculation_number} is not found"
        student_id = student_id_result[0]

        cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
        course_id_result = cursor.fetchone()
        if not course_id_result:
            return f"Course with name {course_name} is not found"
        course_id = course_id_result[0]

        cursor.execute('SELECT id FROM exams WHERE course_id = ?', (course_id,))
        exam_id_result = cursor.fetchone()
        if not exam_id_result:
            return f"{course_name} exam is not found"
        exam_id = exam_id_result[0]

        cursor.execute('SELECT grade FROM student_exam_grades WHERE exam_id = ? AND student_id = ?', (exam_id, student_id))
        student_exam_grade_result = cursor.fetchone()
        if not student_exam_grade_result:
            return "Exam is not passed"
        student_exam_grade = student_exam_grade_result[0]
        return f"Your grade for {course_name} exam is {student_exam_grade}"
    except Exception as e:
        return f"An error occurred while quering the exam grade: {str(e)}"
    
def query_student_profile(matriculation_number):
    print(f'LOG query_student_profile: Query student profile for {matriculation_number}')

    try:
        cursor.execute('SELECT id, first_name, last_name, matriculation_number FROM students WHERE matriculation_number = ?', (matriculation_number,))
        student_result = cursor.fetchone()
        if not student_result:
            return f"{matriculation_number} exam is not found"
        student_id, first_name, last_name, matriculation_number = student_result

        cursor.execute('SELECT address, city, post_code FROM student_address WHERE student_id = ?', (student_id,))
        student_address_result = cursor.fetchone()
        if not student_address_result:
            return f"{matriculation_number}'s address is not found"
        address, city, post_code = student_address_result

        cursor.execute("""   
            SELECT 
                c.name AS course_name, 
                seg.grade AS exam_grade
            FROM 
                student_exam_grades seg
            JOIN 
                exams e ON seg.exam_id = e.id
            JOIN 
                courses c ON e.course_id = c.id
            WHERE 
                seg.student_id = ?
        """, (student_id,))
        grades_result = cursor.fetchall()
        if not grades_result:
            grades_output = "No grades available"
        else:
            grades_output = "\n".join([f"{course}: {grade}" for course, grade in grades_result])

        cursor.execute("""   
            SELECT 
                c.name AS course_name, 
                e.time AS exam_time
            FROM 
                exams e
            JOIN 
                courses c ON e.course_id = c.id
            WHERE 
                e.time > datetime('now') AND e.id IN (
                    SELECT exam_id FROM student_exams WHERE student_id = ?
                )
        """, (student_id,))
        future_exams_result = cursor.fetchall()
        if not future_exams_result:
            exams_output = "No future exams"
        else:
            exams_output = "\n".join([f"{course} on {time}" for course, time in future_exams_result])

        return (
            f"Student: {matriculation_number}, {first_name} {last_name}. "
            f"Address: {address}, {post_code}, {city}. "
            f"\nExams:\n{exams_output}. "
            f"\nGrades:\n{grades_output} "
        )

    except Exception as e:
        return f"An error occurred while querying the student profile: {str(e)}"
    
actions = {    
    "change_first_name": change_first_name,
    "change_last_name": change_last_name,
    "change_address": change_address,
    "register_exam": register_exam,
    "deregister_exam": deregister_exam,
    "query_exam_status": query_exam_status,
    "query_exam_grade": query_exam_grade,
    "query_student_profile": query_student_profile
}
