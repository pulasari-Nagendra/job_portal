CREATE DATABASE IF NOT EXISTS job_portal;
USE job_portal;

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('candidate', 'employer') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- JOBS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(150) NOT NULL,
    salary DECIMAL(10,2) NULL,
    description TEXT NOT NULL,
    requirements TEXT NOT NULL,
    job_type ENUM('Full-time', 'Part-time', 'Internship') NOT NULL,
    employer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_jobs_employer
        FOREIGN KEY (employer_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =========================
-- APPLICATIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    candidate_id INT NOT NULL,
    status ENUM('Applied', 'Shortlisted', 'Rejected')
        DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_applications_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_applications_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_application
        UNIQUE (job_id, candidate_id)
);