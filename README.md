# Library Management System

A Django-based library management system with a request-based book issuing workflow. Students request books, and librarians approve/reject requests before issuing books.

## Features

- Role-based authentication (librarian/student)
- Book inventory management with total/available copies tracking
- Request-based book issuing workflow:
  - Students request books
  - Librarians approve/reject requests
  - Librarians issue approved books
  - Students return books
- Librarian dashboard for managing all requests
- Student dashboard for viewing requests and issued books
- Admin panel for managing books and users

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`

## Usage

### Librarian Workflow
1. Login as librarian
2. View all book requests on the librarian dashboard
3. Approve or reject student requests
4. Issue books for approved requests
5. Manage book returns

### Student Workflow
1. Login as student
2. Browse available books
3. Request books (if available copies > 0)
4. View request status
5. Return issued books

## Demo Credentials

- Librarian: librarian / lib123
- Student 1: student1 / stu123
- Student 2: student2 / stu123
