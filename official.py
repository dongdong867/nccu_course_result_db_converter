import os
import sqlite3
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
YEARSEM = os.getenv("YEARSEM")
FILENAME = os.getenv("FILENAME")

official_df = pd.read_excel(
    FILENAME,
    header=None,
    dtype=str,
    skiprows=[0, 1, 2, 3, 4],
    usecols=[0, 1, 2, 3, 4, 5],
    names=[
        "courseId",
        "name",
        "time",
        "studentLimit",
        "studentCount",
        "lastEnroll",
    ],
)
official_df.fillna("-1", inplace=True)

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS TEST_RESULT (
        courseId TEXT NOT NULL,
        yearsem TEXT,
        name TEXT,
        teacher TEXT,
        time TEXT,
        studentLimit INT,
        studentCount INT,
        lastEnroll INT,
        PRIMARY KEY ( courseId )
    );
"""
)

for course in official_df.head().iterrows():
    cur.execute("SELECT teacher FROM COURSE WHERE id = ?", (YEARSEM + course[1][0],))
    teacher = cur.fetchone()
    teacher = teacher[0]

    cur.execute(
        "INSERT OR REPLACE INTO TEST_RESULT VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            YEARSEM + course[1][0],
            YEARSEM,
            course[1][1],
            teacher,
            course[1][2],
            course[1][3],
            course[1][4],
            course[1][5],
        ),
    )
    con.commit()

con.close()
