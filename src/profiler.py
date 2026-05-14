from pathlib import Path
import sqlite3
import logging

def run_data_profile(db_path):
    db_path = Path(db_path)

    if not db_path.is_file():
        logging.error(f"Failed to profile: {db_path} | Reason: database not found at {db_path}")
        return

    try:
        database = sqlite3.connect(db_path)
        cursor = database.cursor()

        total          = fetch_from_database_query(cursor, "SELECT COUNT(*) from jobs")
        null_job_title = fetch_from_database_query(cursor, "SELECT COUNT(*) from jobs WHERE job_title IS NULL")
        null_company   = fetch_from_database_query(cursor, "SELECT COUNT(*) from jobs WHERE company IS NULL")
        null_desc      = fetch_from_database_query(cursor, "SELECT COUNT(*) from jobs WHERE description IS NULL")
        avg_desc       = fetch_from_database_query(cursor, "SELECT CAST(ROUND(AVG(LENGTH(description))) AS INTEGER) from jobs")

        shortest       = fetch_from_database_query(cursor, """
                                                        SELECT source_id, job_title, LENGTH(description)
                                                        FROM jobs
                                                        WHERE LENGTH(description) = (
                                                        SELECT MIN(LENGTH(description)) FROM jobs
                                                        )
                                                        """)
        longest        = fetch_from_database_query(cursor, """
                                                        SELECT source_id, job_title, LENGTH(description)
                                                        FROM jobs
                                                        WHERE LENGTH(description) = (
                                                        SELECT MAX(LENGTH(description)) FROM jobs
                                                        )
                                                        """)
        shortest_desc_id    = shortest[0]
        shortest_desc_title = shortest[1]
        shortest_desc       = shortest[2]
        longest_desc_id     = longest[0]
        longest_desc_title  = longest[1]
        longest_desc        = longest[2]

        database.close()

        print(
            "--- 🔍 DATA QUALITY REPORT ---",
            f"📈 Total Records: {total}",
            f"❓ Missing Values -> job_title: {null_job_title}, company: {null_company}, description: {null_desc}",
            f"📝 Avg Description Length: {avg_desc} chars",
            f"⚠️  Shortest Description: {shortest_desc} chars",
            f"  ↳ source_id: {shortest_desc_id} | job_title: {shortest_desc_title}",
            f"🚨 Longest Description: {longest_desc} chars",
            f"  ↳ source_id: {longest_desc_id} | job_title: {longest_desc_title}",
            sep="\n")
    except Exception as e:
        logging.error(f"Failed to profile: {db_path} | Reason: {e}")

def fetch_from_database_query(cursor, query):
    cursor.execute(query)
    output = cursor.fetchone()
    if len(output) == 1:
        return output[0]
    return output