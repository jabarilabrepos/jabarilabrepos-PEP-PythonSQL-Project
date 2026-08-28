# PEP Python SQL Project

A Python and SQL data-processing application developed as part of Revature's Python with Data Pre-Training program.

The project simulates a call center data-management system. It loads user and call-log data from CSV files, validates and cleans the records, stores the data in an in-memory SQLite database, performs SQL-based analytics, and exports the processed results to new CSV files.

## Features

- Loads user and call-log data from CSV files
- Validates incoming records and removes incomplete or malformed data
- Stores cleaned data in an in-memory SQLite database
- Maintains a relationship between users and their call records
- Calculates average call duration and total calls for each user
- Orders call records by user and start time
- Exports analytical results and ordered call data to CSV files

## Data Flow

Raw CSV Data  
→ Validation & Cleaning  
→ SQLite Database  
→ SQL Queries & Analytics  
→ Generated CSV Reports

## Technologies

- Python
- SQL
- SQLite
- CSV
- Python File I/O

## Project Structure

    resources/
        users.csv
        callLogs.csv
        userAnalytics.csv
        orderedCalls.csv

    src/
        main/
            __init__.py
            main.py
        test/
            __init__.py

    README.md

## How It Works

### 1. Data Ingestion

The application reads user and call-log information from CSV files located in the `resources` directory.

### 2. Data Cleaning

Each record is validated before being inserted into the database. Records with missing values or an incorrect number of fields are excluded from processing.

### 3. Database Storage

The application creates an in-memory SQLite database containing two tables:

- `users` — stores user IDs, first names, and last names
- `callLogs` — stores call information including phone number, start time, end time, direction, and associated user ID

The call-log table uses a foreign key relationship to associate each call with a user.

### 4. Data Analytics

SQL queries are used to calculate:

- Average call duration for each user
- Total number of calls for each user

The application also sorts call records by user ID and call start time.

### 5. Output

Processed results are exported into:

- `userAnalytics.csv` — contains each user's average call duration and total number of calls
- `orderedCalls.csv` — contains call records ordered by user and start time

## Running the Project

This project uses Python's built-in `sqlite3` and `csv` modules, so no external database server is required.

Run the application from the project directory:

    python src/main/main.py

The application will process the source CSV files, perform the required database operations and analytics, and generate the output CSV files in the `resources` directory.

## What I Practiced

This project provided hands-on experience with:

- Python backend development
- SQL queries and relational database concepts
- Data ingestion and transformation
- Data validation and cleaning
- SQLite database operations
- CSV file processing
- Generating analytical outputs from structured data

## Author

Jabari Robinson

Developed as part of Revature's Python with Data Pre-Training program.
