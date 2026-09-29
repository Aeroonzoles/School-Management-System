

# School Management System

A menu-driven School Management System developed using Python and MySQL as a CBSE Class 12 Computer Science project.

The application provides a centralized system for managing student records, teacher records, academic results, attendance, and fee payments through a relational MySQL database.

## Features

### Student Management
- Admit new students
- View student details
- Display all students
- Update student information
- Delete student records
- Search students by name or roll number

### Teacher Management
- Add teachers
- View teacher details
- Display all teachers
- Update teacher information
- Delete teacher records

### Marks & Result Management
- Enter and update student marks
- Generate student report cards
- Display class results
- Find the class topper
- Generate subject-wise statistics
- Generate pass/fail summaries
- Calculate total marks, percentage, grade, and result

### Attendance Management
- Mark daily attendance
- Record Present, Absent, and Late status
- View attendance by date
- Generate individual attendance reports
- Generate class attendance summaries
- Calculate attendance percentage
- Display a warning when attendance falls below 75%

### Fee Management
- Record fee payments
- Generate receipt numbers
- View fee receipts by student
- Generate fee collection reports by date
- Record fee type, amount, and payment mode

## Technology Stack

- Python
- MySQL
- mysql-connector-python
- python-dotenv

## Database

The application uses a MySQL database named `school_db`.

The system automatically creates the database and required tables when the application is initialized.

### Main Tables

- `students`
- `teachers`
- `marks`
- `attendance`
- `fees`

The academic, attendance, and fee tables use foreign-key relationships with the student records. Related records are automatically removed when a student is deleted.

## Project Structure

```text
School management system/
│
├── school_management.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md\

## Screenshots

### Main Menu

![Main Menu](screenshots/MainMenu.png)

### Student Management

![Student Management](screenshots/StudentManagement.png)

### Marks & Result Management

![Marks & Results](screenshots/Marks.png)

### Attendance Management

![Attendance Management](screenshots/Attendance.png)

### Fee Management

![Fee Management](screenshots/FeeManagement.png)