import csv
import os
import sqlite3

# Resolve the resources folder relative to this file, so paths work
# no matter what directory the script is run from.
_RESOURCES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    '..',
    'resources'
)

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # Load and clean data
    load_and_clean_users(
        os.path.join(_RESOURCES_DIR, 'users.csv')
    )

    load_and_clean_call_logs(
        os.path.join(_RESOURCES_DIR, 'callLogs.csv')
    )

    # Write output files
    write_user_analytics(
        os.path.join(_RESOURCES_DIR, 'userAnalytics.csv')
    )

    write_ordered_calls(
        os.path.join(_RESOURCES_DIR, 'orderedCalls.csv')
    )

    # Helper method for debugging/validation.
    # Uncomment to see data in the database.
    # select_from_users_and_call_logs()

    # Close the cursor and connection
    cursor.close()
    conn.close()


# This function will load the users.csv file into the users table,
# discarding any records with incomplete data.
def load_and_clean_users(file_path):

    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader, None)

        for row in reader:

            # users table requires exactly 3 fields
            if len(row) != 3:
                continue

            # Skip rows containing empty values
            if any(value.strip() == '' for value in row):
                continue

            cursor.execute(
                '''INSERT INTO users (userId, firstName, lastName)
                   VALUES (?, ?, ?)''',
                (row[0], row[1], row[2])
            )

    conn.commit()


# This function will load the callLogs.csv file into the callLogs table,
# discarding any records with incomplete data.
def load_and_clean_call_logs(file_path):

    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader, None)

        for row in reader:

            # callLogs table requires exactly 6 fields
            if len(row) != 6:
                continue

            # Skip rows containing empty values
            if any(value.strip() == '' for value in row):
                continue

            cursor.execute(
                '''INSERT INTO callLogs
                   (callId, phoneNumber, startTime, endTime, direction, userId)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (row[0], row[1], row[2], row[3], row[4], row[5])
            )

    conn.commit()


# This function will write analytics data to userAnalytics.csv.
def write_user_analytics(csv_file_path):

    cursor.execute('''
        SELECT
            userId,
            AVG(endTime - startTime) AS avgDuration,
            COUNT(*) AS numCalls
        FROM callLogs
        GROUP BY userId
        ORDER BY userId
    ''')

    results = cursor.fetchall()

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            'userId',
            'avgDuration',
            'numCalls'
        ])

        # Write analytics data
        for row in results:
            writer.writerow(row)


# This function will write the callLogs ordered by userId,
# then start time.
def write_ordered_calls(csv_file_path):

    cursor.execute('''
        SELECT *
        FROM callLogs
        ORDER BY userId, startTime
    ''')

    results = cursor.fetchall()

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            'callId',
            'phoneNumber',
            'startTime',
            'endTime',
            'direction',
            'userId'
        ])

        # Write ordered call logs
        for row in results:
            writer.writerow(row)


# This function is for debugging/validation.
# Uncomment the function invocation in main() to see the data.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')

    for row in cursor:
        print(row)

    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')

    for row in cursor:
        print(row)


# Required by the tests
def return_cursor():
    return cursor


if __name__ == '__main__':
    main()