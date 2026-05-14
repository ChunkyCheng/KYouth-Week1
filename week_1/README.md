# KYouth Week 1 — Data Engineering Pipeline

## Overview

This project builds a local data engineering pipeline that:

- Extracts raw job data from `.mhtml` files  
- Processes and cleans HTML into structured JSON  
- Loads cleaned data into a relational SQLite database (`jobs.db`)  

The pipeline is orchestrated via a CLI tool (`main.py`) that supports a multi-stage ETL workflow.

---

## Pipeline Architecture

The data flows through 4 stages:

0_source/   → raw .mhtml files  
1_bronze/   → extracted HTML  
2_silver/   → cleaned structured JSON  
3_gold/     → SQLite database (jobs.db)  

Each stage is idempotent and can be rerun independently via CLI commands.

---

## Requirements

- Python 3.14
- uv (version 0.8.* recommended)

Install `uv`:
https://docs.astral.sh/uv/getting-started/installation/

---

## Setup

Run the project (uv handles dependencies automatically):

uv run main.py  

---

## Usage

All commands are executed through main.py:

Show available commands:

uv run main.py  

---

### Ingest

Extract `.mhtml` files into raw HTML:

uv run main.py ingest  

0_source/*.mhtml → 1_bronze/*.html  

---

### Process

Clean HTML and convert into structured JSON:

uv run main.py process  

1_bronze/*.html → 2_silver/*.json  

---

### Load

Load processed JSON into SQLite database:

uv run main.py load  

2_silver/*.json → 3_gold/jobs.db  

---

### Profile

Run basic analysis on the database:

uv run main.py profile  

---

## Output Database Schema

The final SQLite database contains a `jobs` table:

- source_id — primary key
- job_title — title of job posting  
- company — company name  
- description — cleaned readable text  

---

### Module 1: The Extractor (Medallion & Lakehouses)
Why is it useful to keep the original raw HTML files instead of directly inserting processed data into the database? What problems become easier to debug or recover from?
- **Answer**: Keeping the original means you always have something to fall back to. If any mistake was made that changed or lost information, the original will be there.

### Module 2: Treatment Plant (ETL vs ELT & Scale)
Why do cloud systems prefer loading raw data first before cleaning it (ELT)? What problems happen when processing files sequentially, and how does distributed processing help?
- **Answer**: Cloud systems are able to store data cheaply and can transform it only when needed. Processing files sequentially slows down the process as each step relies on the previous where one failure can stop the entire pipeline. Distributed processing allows for parallel tasks.

### Module 3: The Blueprint & The Vault (Storage & Contracts)
What should happen if an important field like job_title disappears? Why fail early instead of silently inserting nulls into DB? How does INSERT OR IGNORE help prevent duplicate records?
- **Answer**: Silent nulls in important fields reduce the reliability, trust and quality of a database. It should be handled now rather than later. INSERT and IGNORE prevents duplicates and missing primary keys.

### Module 4: The QA Inspector & Orchestrator (Orchestration & DAGs)
What happens if processor.py crashes halfway? How are automated orchestration tools more reliable than manual retries with Python scripts?
- **Answer**: If processor.py crashes halfway, you can end up with partial or inconsistent outputs that are hard to track manually. Automated orchestration tools solve this by managing dependencies, retries, and checkpoints so tasks resume safely. They are more reliable than manual scripts because they enforce execution order and can recover from failures without human intervention.