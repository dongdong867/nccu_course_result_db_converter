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
    CREATE TABLE IF NOT EXISTS RESULT (
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

for pos in range(len(official_df)):
    cur.execute(
        "SELECT teacher FROM COURSE WHERE id = ?", (YEARSEM + official_df.iloc[pos, 0],)
    )
    teacher = cur.fetchone()
    teacher = teacher[0]

    cur.execute(
        "INSERT OR REPLACE INTO TEST_RESULT VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            YEARSEM + official_df.iloc[pos, 0],
            YEARSEM,
            official_df.iloc[pos, 1],
            teacher,
            official_df.iloc[pos, 2],
            official_df.iloc[pos, 3],
            official_df.iloc[pos, 4],
            official_df.iloc[pos, 5],
        ),
    )
    con.commit()

con.close()
