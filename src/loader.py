from pathlib import Path
import sqlite3
import json

def load_all_jsons(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    database = sqlite3.connect(output_dir / "jobs.db")
    cursor = database.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
    source_id TEXT PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    description TEXT,
    tech_stack TEXT
    )
    """)

    total = 0
    success = 0
    fail = 0
    print("🥇 Gold: ", output_dir, "/", sep="")
    for f in input_dir.iterdir():
        if f.is_file() and f.suffix == ".json":
            total += 1
            if load_json(f, cursor):
                success += 1
            else:
                fail += 1
    database.commit()
    database.close()

    print("\n📊 Gold Summary:\nTotal:", total, "| Inserted:", success, "| Skipped:", fail)

def load_json(file, cursor):
    data = json.loads(file.read_text())

    try:
        cursor.execute("""
        INSERT INTO jobs (source_id, job_title, company, description)
        VALUES (?,?,?,?)
        """,
        (data["source_id"], data["job_title"], data["company"], data["description"])
        )
        print("✅ Inserted:", file.name)
    except sqlite3.IntegrityError as e:
        print("⏭️ Skipped (duplicate):", file.name)
        return False

    return True