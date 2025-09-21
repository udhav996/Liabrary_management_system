-- schema.sql

-- Create the database
CREATE DATABASE IF NOT EXISTS library_manager;
USE library_manager;

-- Table: students
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    address VARCHAR(255),
    photo_path VARCHAR(255),
    library_id VARCHAR(50) UNIQUE,
    barcode VARCHAR(100) UNIQUE
);

-- Table: books
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150),
    author VARCHAR(100),
    subject VARCHAR(100),
    barcode VARCHAR(100) UNIQUE,
    quantity INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    location VARCHAR(100),
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: issued_books
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(100), -- changed from INT because you map to library_id
    book_barcode VARCHAR(100),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date DATE DEFAULT NULL,
    status VARCHAR(20) DEFAULT 'Issued',
    FOREIGN KEY (student_id) REFERENCES students(library_id),
    FOREIGN KEY (book_barcode) REFERENCES books(barcode)
);

-- Table: logs
CREATE TABLE IF NOT EXISTS logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action TEXT,
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: users (for login/auth if needed)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);
