# ============================================================
#  SCHOOL MANAGEMENT SYSTEM
#  CBSE Class 12 Computer Science Investigatory Project
#  Topics Covered: Python-MySQL Connectivity, File Handling,
#                  Functions, Lists, Dictionaries, OOP Concepts
# ============================================================
#
#  REQUIREMENTS:
#    pip install mysql-connector-python
#
#  MYSQL SETUP (run these in MySQL before starting):
#    CREATE DATABASE school_db;
#    CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_password';
#    GRANT ALL PRIVILEGES ON school_db.* TO 'root'@'localhost';
#
#  HOW TO RUN:
#    python school_management.py
# ============================================================

import mysql.connector
from datetime import datetime, date
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
# ─────────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────────

def connect_db():
    """Establish connection to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin"      # Change your password
        )

        cursor = conn.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS school_db")

        # Select database
        cursor.execute("USE school_db")

        cursor.close()
        return conn

    except mysql.connector.Error as e:
        print(f"\n  [ERROR] Cannot connect to MySQL: {e}")
        print("  Make sure MySQL is running and credentials are correct.\n")
        exit()

# ─────────────────────────────────────────────
#  DATABASE & TABLE INITIALIZATION
# ─────────────────────────────────────────────

def initialize_database():
    """Create all required tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # ── Students Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id   INT AUTO_INCREMENT PRIMARY KEY,
            roll_no      VARCHAR(20)  NOT NULL UNIQUE,
            name         VARCHAR(100) NOT NULL,
            class        VARCHAR(10)  NOT NULL,
            section      VARCHAR(5)   NOT NULL,
            gender       VARCHAR(10),
            dob          DATE,
            phone        VARCHAR(15),
            email        VARCHAR(100),
            address      TEXT,
            admission_date DATE,
            status       VARCHAR(20)  DEFAULT 'Active'
        )
    """)

    # ── Teachers Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id   INT AUTO_INCREMENT PRIMARY KEY,
            emp_code     VARCHAR(20)  NOT NULL UNIQUE,
            name         VARCHAR(100) NOT NULL,
            subject      VARCHAR(50),
            class_incharge VARCHAR(20),
            phone        VARCHAR(15),
            email        VARCHAR(100),
            salary       DECIMAL(10,2),
            join_date    DATE,
            status       VARCHAR(20)  DEFAULT 'Active'
        )
    """)

    # ── Marks Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            mark_id      INT AUTO_INCREMENT PRIMARY KEY,
            roll_no      VARCHAR(20)  NOT NULL,
            student_name VARCHAR(100),
            class        VARCHAR(10),
            exam_type    VARCHAR(30),
            english      INT DEFAULT 0,
            mathematics  INT DEFAULT 0,
            science      INT DEFAULT 0,
            social_science INT DEFAULT 0,
            computer     INT DEFAULT 0,
            total        INT,
            percentage   DECIMAL(5,2),
            grade        VARCHAR(10),
            result       VARCHAR(10),
            exam_date     DATE,
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
        )
    """)

    # ── Attendance Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            att_id       INT AUTO_INCREMENT PRIMARY KEY,
            roll_no      VARCHAR(20)  NOT NULL,
            student_name VARCHAR(100),
            class        VARCHAR(10),
            att_date     DATE         NOT NULL,
            status       VARCHAR(15)  DEFAULT 'Present',
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
        )
    """)

    # ── Fee Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            fee_id       INT AUTO_INCREMENT PRIMARY KEY,
            roll_no      VARCHAR(20)  NOT NULL,
            student_name VARCHAR(100),
            class        VARCHAR(10),
            fee_type     VARCHAR(50),
            amount       DECIMAL(10,2),
            paid_date    DATE,
            payment_mode VARCHAR(30),
            receipt_no   VARCHAR(30),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("  [✓] Database initialized successfully.")

# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

LINE  = "=" * 72
LINE2 = "-" * 72

def print_header(title):
    print("\n" + LINE)
    print(f"  {title.upper()}")
    print(LINE)

def get_grade(percentage):
    if percentage >= 91: return "A1"
    elif percentage >= 81: return "A2"
    elif percentage >= 71: return "B1"
    elif percentage >= 61: return "B2"
    elif percentage >= 51: return "C1"
    elif percentage >= 41: return "C2"
    elif percentage >= 33: return "D"
    else: return "E (Fail)"

def get_result(marks_list):
    return "FAIL" if any(m < 33 for m in marks_list) else "PASS"

def pause():
    input("\n  Press Enter to continue...")

# ─────────────────────────────────────────────
#  MODULE 1 — STUDENT MANAGEMENT
# ─────────────────────────────────────────────

def student_menu():
    while True:
        print_header("Student Management")
        print("   1. Admit New Student")
        print("   2. View Student Details")
        print("   3. Display All Students")
        print("   4. Update Student Info")
        print("   5. Delete Student Record")
        print("   6. Search Student")
        print("   0. Back to Main Menu")
        print(LINE)
        ch = input("  Enter choice: ").strip()
        if   ch == "1": admit_student()
        elif ch == "2": view_student()
        elif ch == "3": display_all_students()
        elif ch == "4": update_student()
        elif ch == "5": delete_student()
        elif ch == "6": search_student()
        elif ch == "0": break
        else: print("  [!] Invalid choice.")

def admit_student():
    print_header("Admit New Student")
    conn   = connect_db()
    cursor = conn.cursor()

    roll = input("  Roll Number      : ").strip()
    # Check duplicate
    cursor.execute("SELECT roll_no FROM students WHERE roll_no = %s", (roll,))
    if cursor.fetchone():
        print(f"  [!] Roll No {roll} already exists.")
        cursor.close(); conn.close(); return

    name    = input("  Full Name        : ").strip().title()
    cls     = input("  Class            : ").strip()
    section = input("  Section          : ").strip().upper()
    gender  = input("  Gender (M/F/O)   : ").strip().upper()
    dob     = input("  Date of Birth (YYYY-MM-DD) : ").strip()
    phone   = input("  Phone Number     : ").strip()
    email   = input("  Email Address    : ").strip()
    address = input("  Address          : ").strip()

    try:
        cursor.execute("""
            INSERT INTO students (roll_no, name, class, section, gender, dob, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (roll, name, cls, section, gender, dob or None, phone, email, address))
        conn.commit()
        print(f"\n  ✓ Student '{name}' admitted successfully! (Roll No: {roll})")
    except mysql.connector.Error as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close(); conn.close()
    pause()

def view_student():
    print_header("View Student Details")
    roll   = input("  Enter Roll Number: ").strip()
    conn   = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll,))
    s = cursor.fetchone()
    cursor.close(); conn.close()

    if not s:
        print(f"  [!] No student found with Roll No: {roll}")
    else:
        print("\n" + "+" + "-" * 50 + "+")
        print(f"  Student ID     : {s['student_id']}")
        print(f"  Roll Number    : {s['roll_no']}")
        print(f"  Name           : {s['name']}")
        print(f"  Class-Section  : {s['class']}-{s['section']}")
        print(f"  Gender         : {s['gender']}")
        print(f"  Date of Birth  : {s['dob']}")
        print(f"  Phone          : {s['phone']}")
        print(f"  Email          : {s['email']}")
        print(f"  Address        : {s['address']}")
        print(f"  Admission Date : {s['admission_date']}")
        print(f"  Status         : {s['status']}")
        print("+" + "-" * 50 + "+")
    pause()

def display_all_students():
    print_header("All Students")
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name, class, section, gender, phone, status FROM students ORDER BY class, roll_no")
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print("  [!] No student records found.")
    else:
        print(f"\n  Total Students: {len(rows)}\n")
        print(f"  {'Roll':<8} {'Name':<22} {'Class':<6} {'Sec':<5} {'Gender':<8} {'Phone':<13} Status")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]:<6} {r[3]:<5} {r[4]:<8} {r[5]:<13} {r[6]}")
    pause()

def update_student():
    print_header("Update Student Info")
    roll   = input("  Enter Roll Number to update: ").strip()
    conn   = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll,))
    s = cursor.fetchone()

    if not s:
        print(f"  [!] No student found with Roll No: {roll}")
        cursor.close(); conn.close(); return

    print(f"  Updating: {s['name']} | Class {s['class']}-{s['section']}")
    print("  (Press Enter to keep current value)\n")

    name    = input(f"  Name    [{s['name']}]    : ").strip() or s['name']
    phone   = input(f"  Phone   [{s['phone']}]   : ").strip() or s['phone']
    email   = input(f"  Email   [{s['email']}]   : ").strip() or s['email']
    address = input(f"  Address [{s['address']}] : ").strip() or s['address']
    status  = input(f"  Status  [{s['status']}]  : ").strip() or s['status']

    cursor.execute("""
        UPDATE students SET name=%s, phone=%s, email=%s, address=%s, status=%s
        WHERE roll_no=%s
    """, (name, phone, email, address, status, roll))
    conn.commit()
    print(f"\n  ✓ Student record updated successfully.")
    cursor.close(); conn.close()
    pause()

def delete_student():
    print_header("Delete Student Record")
    roll = input("  Enter Roll Number to delete: ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE roll_no = %s", (roll,))
    row = cursor.fetchone()

    if not row:
        print(f"  [!] No student found with Roll No: {roll}")
        cursor.close(); conn.close(); return

    confirm = input(f"  Delete '{row[0]}' (Roll: {roll})? This also deletes marks/attendance/fees. (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll,))
        conn.commit()
        print(f"  ✓ Student and all related records deleted.")
    else:
        print("  Deletion cancelled.")
    cursor.close(); conn.close()
    pause()

def search_student():
    print_header("Search Student")
    kw   = input("  Enter name or roll number to search: ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT roll_no, name, class, section, phone, status
        FROM students
        WHERE name LIKE %s OR roll_no LIKE %s
    """, (f"%{kw}%", f"%{kw}%"))
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No results for '{kw}'")
    else:
        print(f"\n  Found {len(rows)} record(s):\n")
        print(f"  {'Roll':<8} {'Name':<22} {'Class':<6} {'Sec':<5} {'Phone':<13} Status")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]:<6} {r[3]:<5} {r[4]:<13} {r[5]}")
    pause()

# ─────────────────────────────────────────────
#  MODULE 2 — TEACHER MANAGEMENT
# ─────────────────────────────────────────────

def teacher_menu():
    while True:
        print_header("Teacher Management")
        print("   1. Add New Teacher")
        print("   2. View Teacher Details")
        print("   3. Display All Teachers")
        print("   4. Update Teacher Info")
        print("   5. Delete Teacher Record")
        print("   0. Back to Main Menu")
        print(LINE)
        ch = input("  Enter choice: ").strip()
        if   ch == "1": add_teacher()
        elif ch == "2": view_teacher()
        elif ch == "3": display_all_teachers()
        elif ch == "4": update_teacher()
        elif ch == "5": delete_teacher()
        elif ch == "0": break
        else: print("  [!] Invalid choice.")

def add_teacher():
    print_header("Add New Teacher")
    conn   = connect_db()
    cursor = conn.cursor()

    emp = input("  Employee Code     : ").strip()
    cursor.execute("SELECT emp_code FROM teachers WHERE emp_code = %s", (emp,))
    if cursor.fetchone():
        print(f"  [!] Employee code {emp} already exists.")
        cursor.close(); conn.close(); return

    name    = input("  Full Name         : ").strip().title()
    subject = input("  Subject           : ").strip()
    incharge= input("  Class Incharge Of : ").strip()
    phone   = input("  Phone Number      : ").strip()
    email   = input("  Email             : ").strip()
    salary  = input("  Monthly Salary    : ").strip()

    cursor.execute("""
        INSERT INTO teachers (emp_code, name, subject, class_incharge, phone, email, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (emp, name, subject, incharge, phone, email, float(salary) if salary else 0))
    conn.commit()
    print(f"\n  ✓ Teacher '{name}' added successfully!")
    cursor.close(); conn.close()
    pause()

def view_teacher():
    print_header("View Teacher Details")
    emp    = input("  Enter Employee Code: ").strip()
    conn   = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers WHERE emp_code = %s", (emp,))
    t = cursor.fetchone()
    cursor.close(); conn.close()

    if not t:
        print(f"  [!] No teacher found with code: {emp}")
    else:
        print("\n" + "+" + "-" * 50 + "+")
        for key, val in t.items():
            print(f"  {key.replace('_',' ').title():<18}: {val}")
        print("+" + "-" * 50 + "+")
    pause()

def display_all_teachers():
    print_header("All Teachers")
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT emp_code, name, subject, class_incharge, phone, salary, status FROM teachers")
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print("  [!] No teacher records found.")
    else:
        print(f"\n  Total Teachers: {len(rows)}\n")
        print(f"  {'Code':<8} {'Name':<22} {'Subject':<18} {'Incharge':<10} {'Phone':<13} Salary")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]:<18} {r[3]:<10} {r[4]:<13} {r[5]}")
    pause()

def update_teacher():
    print_header("Update Teacher Info")
    emp    = input("  Enter Employee Code to update: ").strip()
    conn   = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers WHERE emp_code = %s", (emp,))
    t = cursor.fetchone()
    if not t:
        print(f"  [!] No teacher found with code: {emp}")
        cursor.close(); conn.close(); return

    print(f"  Updating: {t['name']}")
    phone  = input(f"  Phone  [{t['phone']}]  : ").strip() or t['phone']
    salary = input(f"  Salary [{t['salary']}] : ").strip() or t['salary']
    status = input(f"  Status [{t['status']}] : ").strip() or t['status']

    cursor.execute("""
        UPDATE teachers SET phone=%s, salary=%s, status=%s WHERE emp_code=%s
    """, (phone, salary, status, emp))
    conn.commit()
    print("  ✓ Teacher record updated.")
    cursor.close(); conn.close()
    pause()

def delete_teacher():
    print_header("Delete Teacher Record")
    emp    = input("  Enter Employee Code to delete: ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM teachers WHERE emp_code = %s", (emp,))
    row = cursor.fetchone()
    if not row:
        print(f"  [!] No teacher found.")
        cursor.close(); conn.close(); return
    confirm = input(f"  Delete '{row[0]}'? (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM teachers WHERE emp_code = %s", (emp,))
        conn.commit()
        print("  ✓ Teacher record deleted.")
    cursor.close(); conn.close()
    pause()

# ─────────────────────────────────────────────
#  MODULE 3 — MARKS / RESULT MANAGEMENT
# ─────────────────────────────────────────────

def marks_menu():
    while True:
        print_header("Marks & Result Management")
        print("   1. Enter / Update Marks")
        print("   2. View Report Card")
        print("   3. Display Class Result")
        print("   4. Class Topper")
        print("   5. Subject-Wise Statistics")
        print("   6. Pass / Fail Summary")
        print("   0. Back to Main Menu")
        print(LINE)
        ch = input("  Enter choice: ").strip()
        if   ch == "1": enter_marks()
        elif ch == "2": view_report_card()
        elif ch == "3": display_class_result()
        elif ch == "4": class_topper()
        elif ch == "5": subject_statistics()
        elif ch == "6": pass_fail_summary()
        elif ch == "0": break
        else: print("  [!] Invalid choice.")

def enter_marks():
    print_header("Enter Student Marks")
    roll = input("  Roll Number  : ").strip()
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, class FROM students WHERE roll_no = %s", (roll,))
    s = cursor.fetchone()
    if not s:
        print(f"  [!] No student with Roll No: {roll}")
        cursor.close(); conn.close(); return

    print(f"  Student: {s['name']} | Class: {s['class']}")
    exam_type = input("  Exam Type (Unit Test/Half Yearly/Annual): ").strip()

    print("\n  Enter marks out of 100:\n")
    subjects = ["english", "mathematics", "science", "social_science", "computer"]
    marks = {}
    for sub in subjects:
        while True:
            try:
                m = int(input(f"    {sub.replace('_',' ').title():<20}: "))
                if 0 <= m <= 100:
                    marks[sub] = m
                    break
                else:
                    print("    [!] Enter 0–100.")
            except ValueError:
                print("    [!] Enter a valid number.")

    ml         = list(marks.values())
    total      = sum(ml)
    percentage = round(total / 5, 2)
    grade      = get_grade(percentage)
    result     = get_result(ml)

    # Check if record exists
    cursor.execute("SELECT mark_id FROM marks WHERE roll_no=%s AND exam_type=%s", (roll, exam_type))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE marks SET english=%s, mathematics=%s, science=%s,
            social_science=%s, computer=%s, total=%s, percentage=%s,
            grade=%s, result=%s, exam_date=CURDATE()
            WHERE roll_no=%s AND exam_type=%s
        """, (*ml, total, percentage, grade, result, roll, exam_type))
        print("\n  ✓ Marks updated.")
    else:
        cursor.execute("""
            INSERT INTO marks (roll_no, student_name, class, exam_type,
            english, mathematics, science, social_science, computer,
            total, percentage, grade, result)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (roll, s['name'], s['class'], exam_type, *ml, total, percentage, grade, result))
        print("\n  ✓ Marks saved.")

    conn.commit()
    cursor.close(); conn.close()
    pause()

def view_report_card():
    print_header("Student Report Card")
    roll      = input("  Roll Number  : ").strip()
    exam_type = input("  Exam Type    : ").strip()
    conn      = connect_db()
    cursor    = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM marks WHERE roll_no=%s AND exam_type=%s", (roll, exam_type))
    m = cursor.fetchone()
    cursor.close(); conn.close()

    if not m:
        print(f"  [!] No marks found for Roll No {roll} | Exam: {exam_type}")
    else:
        print("\n" + "+" + "-" * 58 + "+")
        print("|{:^58}|".format("STUDENT REPORT CARD"))
        print("|{:^58}|".format(f"Exam: {m['exam_type']}"))
        print("+" + "-" * 58 + "+")
        print(f"  Roll No    : {m['roll_no']}")
        print(f"  Name       : {m['student_name']}")
        print(f"  Class      : {m['class']}")
        print(f"  Exam Date  : {m['exam_date']}")
        print("  " + "-" * 40)
        subjects = [("English","english"),("Mathematics","mathematics"),
                    ("Science","science"),("Social Science","social_science"),
                    ("Computer","computer")]
        for label, key in subjects:
            print(f"  {label:<22} : {m[key]:>5} / 100")
        print("  " + "-" * 40)
        print(f"  {'Total':<22} : {m['total']:>5} / 500")
        print(f"  {'Percentage':<22} : {m['percentage']:>5}%")
        print(f"  {'Grade':<22} : {m['grade']}")
        print(f"  {'Result':<22} : {m['result']}")
        print("+" + "-" * 58 + "+")
    pause()

def display_class_result():
    print_header("Class Result")
    cls       = input("  Class         : ").strip()
    exam_type = input("  Exam Type     : ").strip()
    conn      = connect_db()
    cursor    = conn.cursor()
    cursor.execute("""
        SELECT roll_no, student_name, english, mathematics, science,
               social_science, computer, total, percentage, grade, result
        FROM marks WHERE class=%s AND exam_type=%s ORDER BY percentage DESC
    """, (cls, exam_type))
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print("  [!] No records found.")
    else:
        print(f"\n  Class {cls} | {exam_type} | Total: {len(rows)} students\n")
        print(f"  {'Roll':<8} {'Name':<18} {'Eng':>4} {'Mat':>4} {'Sci':>4} {'SS':>4} {'Comp':>5} {'Tot':>5} {'%':>6} {'Grd':>4} Result")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<8} {r[1]:<18} {r[2]:>4} {r[3]:>4} {r[4]:>4} {r[5]:>4} {r[6]:>5} {r[7]:>5} {r[8]:>6} {r[9]:>4} {r[10]}")
    pause()

def class_topper():
    print_header("Class Topper")
    cls       = input("  Class         : ").strip()
    exam_type = input("  Exam Type     : ").strip()
    conn      = connect_db()
    cursor    = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM marks WHERE class=%s AND exam_type=%s
        ORDER BY percentage DESC LIMIT 1
    """, (cls, exam_type))
    t = cursor.fetchone()
    cursor.close(); conn.close()

    if not t:
        print("  [!] No records found.")
    else:
        print(f"\n  🏆 TOPPER of Class {cls} ({exam_type})")
        print(f"\n  Name       : {t['student_name']}")
        print(f"  Roll No    : {t['roll_no']}")
        print(f"  Total      : {t['total']} / 500")
        print(f"  Percentage : {t['percentage']}%")
        print(f"  Grade      : {t['grade']}")
    pause()

def subject_statistics():
    print_header("Subject-Wise Statistics")
    cls       = input("  Class     : ").strip()
    exam_type = input("  Exam Type : ").strip()
    conn      = connect_db()
    cursor    = conn.cursor()
    subjects  = [("English","english"),("Mathematics","mathematics"),
                 ("Science","science"),("Social Science","social_science"),
                 ("Computer","computer")]

    print(f"\n  Class {cls} | {exam_type}\n")
    print(f"  {'Subject':<22} {'Highest':>8} {'Lowest':>8} {'Average':>9} {'Pass%':>7}")
    print("  " + "-" * 58)

    for label, col in subjects:
        cursor.execute(f"""
            SELECT MAX({col}), MIN({col}), AVG({col}),
                   ROUND(SUM({col}>=33)/COUNT(*)*100,1)
            FROM marks WHERE class=%s AND exam_type=%s
        """, (cls, exam_type))
        row = cursor.fetchone()
        if row and row[0] is not None:
            print(f"  {label:<22} {row[0]:>8} {row[1]:>8} {float(row[2]):>9.1f} {float(row[3]):>6.1f}%")
    cursor.close(); conn.close()
    pause()

def pass_fail_summary():
    print_header("Pass / Fail Summary")
    cls       = input("  Class     : ").strip()
    exam_type = input("  Exam Type : ").strip()
    conn      = connect_db()
    cursor    = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM marks WHERE class=%s AND exam_type=%s", (cls, exam_type))
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM marks WHERE class=%s AND exam_type=%s AND result='PASS'", (cls, exam_type))
    passed = cursor.fetchone()[0]
    cursor.execute("""
        SELECT roll_no, student_name, percentage FROM marks
        WHERE class=%s AND exam_type=%s AND result='FAIL'
    """, (cls, exam_type))
    failed_rows = cursor.fetchall()
    cursor.close(); conn.close()

    print(f"\n  Class {cls} | {exam_type}")
    print(f"  Total   : {total}")
    print(f"  Passed  : {passed}")
    print(f"  Failed  : {total - passed}")
    if total > 0:
        print(f"  Pass%   : {round(passed/total*100,1)}%")
    if failed_rows:
        print("\n  Failed Students:")
        print(f"  {'Roll':<8} {'Name':<22} Percentage")
        print("  " + "-" * 40)
        for r in failed_rows:
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]}%")
    pause()

# ─────────────────────────────────────────────
#  MODULE 4 — ATTENDANCE MANAGEMENT
# ─────────────────────────────────────────────

def attendance_menu():
    while True:
        print_header("Attendance Management")
        print("   1. Mark Attendance (Today)")
        print("   2. View Attendance by Date")
        print("   3. Student Attendance Report")
        print("   4. Attendance Summary")
        print("   0. Back to Main Menu")
        print(LINE)
        ch = input("  Enter choice: ").strip()
        if   ch == "1": mark_attendance()
        elif ch == "2": view_attendance_by_date()
        elif ch == "3": student_attendance_report()
        elif ch == "4": attendance_summary()
        elif ch == "0": break
        else: print("  [!] Invalid choice.")

def mark_attendance():
    print_header("Mark Attendance")
    cls  = input("  Class   : ").strip()
    sec  = input("  Section : ").strip().upper()
    today = date.today().isoformat()

    conn   = connect_db()
    cursor = conn.cursor()

    # Check if already marked today
    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE class=%s AND att_date=%s
    """, (cls, today))
    if cursor.fetchone()[0] > 0:
        print(f"  [!] Attendance for Class {cls}-{sec} on {today} already marked.")
        cursor.close(); conn.close(); return

    cursor.execute("""
        SELECT roll_no, name FROM students
        WHERE class=%s AND section=%s AND status='Active'
        ORDER BY roll_no
    """, (cls, sec))
    students = cursor.fetchall()

    if not students:
        print(f"  [!] No active students in Class {cls}-{sec}.")
        cursor.close(); conn.close(); return

    print(f"\n  Marking attendance for Class {cls}-{sec} | Date: {today}")
    print("  Enter 'P' for Present, 'A' for Absent, 'L' for Late\n")

    records = []
    for roll, name in students:
        while True:
            s = input(f"  {roll:<10} {name:<22} [P/A/L]: ").strip().upper()
            if s in ("P","A","L"):
                status_map = {"P":"Present","A":"Absent","L":"Late"}
                records.append((roll, name, cls, today, status_map[s]))
                break
            print("    [!] Enter P, A, or L only.")

    cursor.executemany("""
        INSERT INTO attendance (roll_no, student_name, class, att_date, status)
        VALUES (%s,%s,%s,%s,%s)
    """, records)
    conn.commit()
    print(f"\n  ✓ Attendance saved for {len(records)} students.")
    cursor.close(); conn.close()
    pause()

def view_attendance_by_date():
    print_header("View Attendance by Date")
    cls      = input("  Class (or press Enter for all): ").strip()
    att_date = input("  Date (YYYY-MM-DD)             : ").strip()
    conn     = connect_db()
    cursor   = conn.cursor()

    if cls:
        cursor.execute("""
            SELECT roll_no, student_name, class, att_date, status
            FROM attendance WHERE class=%s AND att_date=%s ORDER BY roll_no
        """, (cls, att_date))
    else:
        cursor.execute("""
            SELECT roll_no, student_name, class, att_date, status
            FROM attendance WHERE att_date=%s ORDER BY class, roll_no
        """, (att_date,))
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No attendance records for {att_date}")
    else:
        print(f"\n  Date: {att_date} | Records: {len(rows)}\n")
        print(f"  {'Roll':<8} {'Name':<22} {'Class':<7} Status")
        print("  " + "-" * 50)
        for r in rows:
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]:<7} {r[4]}")
    pause()

def student_attendance_report():
    print_header("Student Attendance Report")
    roll   = input("  Roll Number: ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT att_date, status FROM attendance
        WHERE roll_no=%s ORDER BY att_date
    """, (roll,))
    rows = cursor.fetchall()

    cursor.execute("SELECT name FROM students WHERE roll_no=%s", (roll,))
    s = cursor.fetchone()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No attendance found for Roll No: {roll}")
    else:
        total   = len(rows)
        present = sum(1 for r in rows if r[1] == "Present")
        absent  = sum(1 for r in rows if r[1] == "Absent")
        late    = sum(1 for r in rows if r[1] == "Late")
        pct     = round((present + late) / total * 100, 1)

        print(f"\n  Student  : {s[0] if s else roll}")
        print(f"  Roll No  : {roll}\n")
        print(f"  Total Days Recorded : {total}")
        print(f"  Present             : {present}")
        print(f"  Absent              : {absent}")
        print(f"  Late                : {late}")
        print(f"  Attendance %        : {pct}%")

        if pct < 75:
            print("  ⚠  WARNING: Attendance below 75%!")

        print("\n  --- Last 10 Records ---")
        for r in rows[-10:]:
            print(f"  {r[0]}  →  {r[1]}")
    pause()

def attendance_summary():
    print_header("Attendance Summary")
    cls      = input("  Class : ").strip()
    conn     = connect_db()
    cursor   = conn.cursor()
    cursor.execute("""
        SELECT roll_no, student_name,
               COUNT(*) AS total,
               SUM(status='Present') AS present,
               SUM(status='Absent')  AS absent,
               ROUND(SUM(status IN ('Present','Late'))/COUNT(*)*100,1) AS pct
        FROM attendance WHERE class=%s
        GROUP BY roll_no, student_name ORDER BY pct DESC
    """, (cls,))
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No data for Class {cls}")
    else:
        print(f"\n  Class {cls} Attendance Summary\n")
        print(f"  {'Roll':<8} {'Name':<22} {'Total':>6} {'Present':>8} {'Absent':>7} {'Att%':>6}")
        print("  " + LINE2)
        for r in rows:
            flag = " ⚠" if float(r[5]) < 75 else ""
            print(f"  {r[0]:<8} {r[1]:<22} {r[2]:>6} {r[3]:>8} {r[4]:>7} {r[5]:>5}%{flag}")
    pause()

# ─────────────────────────────────────────────
#  MODULE 5 — FEE MANAGEMENT
# ─────────────────────────────────────────────

def fee_menu():
    while True:
        print_header("Fee Management")
        print("   1. Collect Fee")
        print("   2. View Fee Receipts (by Student)")
        print("   3. Fee Collection Report (by Date)")
        print("   0. Back to Main Menu")
        print(LINE)
        ch = input("  Enter choice: ").strip()
        if   ch == "1": collect_fee()
        elif ch == "2": view_fee_receipts()
        elif ch == "3": fee_collection_report()
        elif ch == "0": break
        else: print("  [!] Invalid choice.")

def collect_fee():
    print_header("Collect Fee")
    roll   = input("  Roll Number  : ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, class FROM students WHERE roll_no=%s", (roll,))
    s = cursor.fetchone()
    if not s:
        print(f"  [!] No student with Roll No: {roll}")
        cursor.close(); conn.close(); return

    print(f"  Student: {s[0]} | Class: {s[1]}")
    fee_type    = input("  Fee Type (Tuition/Exam/Sports/Library): ").strip()
    amount      = input("  Amount (₹)  : ").strip()
    mode        = input("  Payment Mode (Cash/Online/Cheque)     : ").strip()
    receipt_no  = f"REC{datetime.now().strftime('%Y%m%d%H%M%S')}"

    cursor.execute("""
        INSERT INTO fees (roll_no, student_name, class, fee_type, amount, payment_mode, receipt_no)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (roll, s[0], s[1], fee_type, float(amount), mode, receipt_no))
    conn.commit()

    print("\n" + "+" + "-" * 40 + "+")
    print("|{:^40}|".format("FEE RECEIPT"))
    print("+" + "-" * 40 + "+")
    print(f"  Receipt No  : {receipt_no}")
    print(f"  Student     : {s[0]}")
    print(f"  Roll No     : {roll}")
    print(f"  Class       : {s[1]}")
    print(f"  Fee Type    : {fee_type}")
    print(f"  Amount      : ₹{amount}")
    print(f"  Mode        : {mode}")
    print(f"  Date        : {date.today()}")
    print("+" + "-" * 40 + "+")
    cursor.close(); conn.close()
    pause()

def view_fee_receipts():
    print_header("Fee Receipts by Student")
    roll   = input("  Roll Number: ").strip()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT receipt_no, fee_type, amount, payment_mode, paid_date
        FROM fees WHERE roll_no=%s ORDER BY paid_date DESC
    """, (roll,))
    rows = cursor.fetchall()
    cursor.execute("SELECT name FROM students WHERE roll_no=%s", (roll,))
    s = cursor.fetchone()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No fee records for Roll No: {roll}")
    else:
        total_paid = sum(r[2] for r in rows)
        print(f"\n  Student: {s[0] if s else roll} | Roll: {roll}")
        print(f"  Total Paid: ₹{total_paid}\n")
        print(f"  {'Receipt':<22} {'Type':<15} {'Amount':>8} {'Mode':<12} Date")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<22} {r[1]:<15} ₹{r[2]:>7} {r[3]:<12} {r[4]}")
    pause()

def fee_collection_report():
    print_header("Fee Collection Report")
    d      = input("  Date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not d:
        d = date.today().isoformat()
    conn   = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_name, class, fee_type, amount, payment_mode, receipt_no
        FROM fees WHERE paid_date=%s ORDER BY class
    """, (d,))
    rows = cursor.fetchall()
    cursor.close(); conn.close()

    if not rows:
        print(f"  [!] No collections on {d}")
    else:
        total = sum(r[3] for r in rows)
        print(f"\n  Date: {d} | Total Collected: ₹{total} | Records: {len(rows)}\n")
        print(f"  {'Name':<20} {'Class':<7} {'Type':<15} {'Amount':>8} Mode")
        print("  " + LINE2)
        for r in rows:
            print(f"  {r[0]:<20} {r[1]:<7} {r[2]:<15} ₹{r[3]:>7} {r[4]}")
    pause()

# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def main_menu():
    print("\n  Initializing database...")
    initialize_database()

    while True:
        print("\n" + LINE)
        print("         SCHOOL MANAGEMENT SYSTEM")
        print("         CBSE Class 12 — Python + MySQL Project")
        print(LINE)
        print("   1. Student Management")
        print("   2. Teacher Management")
        print("   3. Marks & Result Management")
        print("   4. Attendance Management")
        print("   5. Fee Management")
        print("   0. Exit")
        print(LINE)

        ch = input("  Enter choice: ").strip()
        if   ch == "1": student_menu()
        elif ch == "2": teacher_menu()
        elif ch == "3": marks_menu()
        elif ch == "4": attendance_menu()
        elif ch == "5": fee_menu()
        elif ch == "0":
            print("\n  Thank you for using School Management System. Goodbye!\n")
            break
        else:
            print("  [!] Invalid choice. Enter 0–5.")

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main_menu()

