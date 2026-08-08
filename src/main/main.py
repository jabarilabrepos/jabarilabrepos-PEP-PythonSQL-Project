# This function will load the users.csv file into the users table, discarding any records with incomplete data
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


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
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


# This function will write analytics data to userAnalytics.csv
def write_user_analytics(csv_file_path):
    cursor.execute('''
        SELECT userId,
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
        writer.writerow(['userId', 'avgDuration', 'numCalls'])

        # Write analytics data
        for row in results:
            writer.writerow(row)


# This function will write the callLogs ordered by userId, then start time
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