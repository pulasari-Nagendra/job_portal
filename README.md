# JobSphere – Job Portal

JobSphere is a full-stack job portal web application that connects candidates with employers.

Candidates can create accounts, search for jobs, apply for suitable positions, and track their applications.

Employers can create job postings, manage their jobs, view applicants, and update application statuses.

---

## Features

### Authentication
- Candidate and Employer registration
- Login with JWT authentication
- Password hashing
- Role-based access control

### Candidate
- Browse available jobs
- Search jobs
- View detailed job information
- Apply for jobs
- View submitted applications
- Track application status

### Employer
- Post new jobs
- Edit existing jobs
- Delete jobs
- View posted jobs
- View candidate applications
- Shortlist candidates
- Reject candidates

### Job Information
Each job contains:
- Job title
- Company
- Location
- Salary
- Description
- Requirements
- Job type
- Posted date

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-JWT-Extended

### Database
- MySQL
- MySQL Connector/Python

### Security
- JWT authentication
- Werkzeug password hashing
- Role-based authorization

---

## Project Structure

```text
job_portal/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── schema.sql
│
├── middleware/
│   ├── __init__.py
│   └── auth.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── jobs.py
│   └── applications.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── jobs.html
│   ├── job-details.html
│   ├── candidate-dashboard.html
│   ├── employer-dashboard.html
│   ├── create-job.html
│   ├── edit-job.html
│   └── my-applications.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── auth.js
        ├── jobs.js
        ├── candidate.js
        └── employer.js