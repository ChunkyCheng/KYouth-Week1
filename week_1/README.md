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

Clone the repository:

git clone <repo-url>  
cd <repo-folder>  

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

## Design Notes

- Each stage is separated for debugging and reproducibility  
- Raw data is preserved to allow reprocessing  
- HTML is fully cleaned before storage to ensure readability  
- Designed for local-first execution (no external services required)  

---

