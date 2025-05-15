-- Create Database
CREATE DATABASE IF NOT EXISTS Contact_Form_DB;
USE Contact_Form_DB;

-- Create Submissions Table
CREATE TABLE IF NOT EXISTS Submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email_token VARCHAR(50) NOT NULL,
    email_domain VARCHAR(100) NOT NULL,
    created_on DATE NOT NULL
);

-- Create Email Logs Table
CREATE TABLE IF NOT EXISTS EmailLogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_token VARCHAR(50) NOT NULL,
    sent_on DATETIME NOT NULL,
    status ENUM('SUCCESS', 'FAILED') NOT NULL,
    error_message TEXT,
    FOREIGN KEY (email_token) REFERENCES Submissions(email_token)
);