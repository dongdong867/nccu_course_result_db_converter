import sqlite3
import pandas as pd

### Setup default data ###
default_dcard_df = pd.read_excel("dcard.xlsx")

### Create DCARD table ###
con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS DCARD (
        y TEXT NOT NULL,
        s TEXT NOT NULL,
        name TEXT NOT NULL,
        teacher TEXT NOT NULL,
        time TEXT NOT NULL,
        type TEXT NOT NULL,
        lastEnroll TEXT,
        addOn TEXT,
        PRIMARY KEY ( y, name, teacher, time, type )
    );
"""
)

### Import default_dcard_df to DCARD ###
for course in default_dcard_df.iterrows():
    cur.execute(
        "INSERT OR REPLACE INTO DCARD VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            str(course[1][0])[:3],
            str(course[1][0])[-1],
            course[1][1],
            course[1][2],
            course[1][4],
            course[1][3],
            course[1][5],
            course[1][6],
        ),
    )
    con.commit()

### Create DCARD_VIEW with qrysub data ###
cur.execute(
    """
    CREATE VIEW IF NOT EXISTS DCARD_VIEW AS
    SELECT c.id, c.y, c.s, c.name, c.teacher, c.time, d.lastEnroll, d.addOn
    FROM COURSE c
    JOIN DCARD d
    ON c.y == d.y AND c.s == d.s AND c.teacher == d.teacher AND c.time == d.time;
"""
)
con.commit()

###############################################################################
# Find courses not match in DCARD table (uncomment below block if needed)     #
###############################################################################

# cur.execute(
#     """
#     SELECT d.*
#     FROM DCARD d
#     LEFT JOIN DCARD_VIEW dv
#     ON d.y == dv.y AND d.s == dv.s AND d.teacher == dv.teacher AND d.time == dv.time
#     WHERE dv.id IS NULL;
# """
# )
#
# result = cur.fetchall()
# for row in result:
#     print(row)
