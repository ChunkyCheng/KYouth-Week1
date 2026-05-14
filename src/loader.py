from pathlib import Path
import sqlite3
import json
import logging
import hashlib

def load_all_jsons(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    if not input_dir.is_dir():
        logging.error(f"Failed to load: {input_dir}/ | Reason: {input_dir}/ not found")
        return

    database = sqlite3.connect(output_dir / "jobs.db")
    cursor = database.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
    source_id TEXT PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    description TEXT,
    tech_stack TEXT,
    content_hash TEXT
    )
    """)

    total = 0
    success = 0
    fail = 0
    print("🥇 Gold:...")
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
    hash_input = f"{normalize(data['job_title'])}|{normalize(data['company'])}|{normalize(data['description'])}"
    content_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    cursor.execute("SELECT content_hash FROM jobs WHERE source_id = ?", (data["source_id"],))
    row = cursor.fetchone()

    if row == None:
        cursor.execute("""
        INSERT INTO jobs (source_id, job_title, company, description, content_hash)
        VALUES (?,?,?,?,?)
        """,
        (data["source_id"], data["job_title"], data["company"], data["description"], content_hash)
        )
        logging.info(f"✅ Inserted: {file.name}")
        return True
    
    if row[0] != content_hash:
        cursor.execute("""
        UPDATE jobs
        SET job_title = ?, company = ?, description = ?, content_hash = ?
        WHERE source_id = ?
        """,
        (data["job_title"], data["company"], data["description"], content_hash, data["source_id"])
        )
        logging.info(f"🔄 Updated: {file.name}")
        return True

    logging.warning(f"⏭️ Skipped (duplicate): {file.name}")
    return False

def normalize(text):
	if text is None:
		return ""
	return " ".join(text.lower().split())