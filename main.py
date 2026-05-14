from fastapi import FastAPI, UploadFile, File
from db_connection import get_connection
import csv
import io

app = FastAPI()

@app.post("/upload-grades")
def upload_grades(file: UploadFile = File(...)):
    content = file.file.read()

    csv_file = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    conn = get_connection()
    cursor = conn.cursor()

    records_loaded = 0
    unique_students = set()

    for row in reader:
        full_name = row["full_name"]
        subject = row["subject"]

        if not row["grade"].isdigit():
            continue

        grade = int(row["grade"])

        # validation check
        if grade < 2 or grade > 5:
            continue
        if not full_name.strip() or not subject.strip():
            continue

        cursor.execute("""
            INSERT INTO grades (full_name, subject, grade)
            VALUES (%s, %s, %s)
        """, (full_name, subject, grade))

        records_loaded += 1
        unique_students.add(full_name)

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status": "ok",
        "records_loaded": records_loaded,
        "students": len(unique_students)
    }


@app.get("/students/more-than-3-twos")
def more_than_3_twos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT full_name, COUNT(*) as count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) > 3
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "full_name": row[0],
            "count_twos": row[1]
        })

    cursor.close()
    conn.close()

    return result


@app.get("/students/less-than-5-twos")
def less_than_5_twos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT full_name, COUNT(*) as count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) < 5
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "full_name": row[0],
            "count_twos": row[1]
        })

    cursor.close()
    conn.close()

    return result