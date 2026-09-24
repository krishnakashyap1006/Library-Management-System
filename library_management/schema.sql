CREATE DATABASE IF NOT EXISTS lib_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE lib_management;

CREATE TABLE IF NOT EXISTS books (
    book_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(150) NOT NULL,
    author VARCHAR(150) NOT NULL,
    quantity INT UNSIGNED NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(120) NOT NULL,
    student_branch VARCHAR(100) NOT NULL,
    student_year SMALLINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    book_id INT UNSIGNED NOT NULL,
    student_id INT UNSIGNED NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE NULL,
    status ENUM('issued', 'returned') NOT NULL DEFAULT 'issued',
    CONSTRAINT fk_transactions_book
        FOREIGN KEY (book_id) REFERENCES books(book_id),
    CONSTRAINT fk_transactions_student
        FOREIGN KEY (student_id) REFERENCES students(student_id),
    INDEX idx_transactions_status (status),
    INDEX idx_transactions_student (student_id),
    INDEX idx_transactions_book (book_id)
);
