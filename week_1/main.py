import sys
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
from src.loader import load_all_jsons
from src.profiler import run_data_profile
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def ingest():
    ingest_all_mhtml("data/0_source", "data/1_bronze")

def process():
    process_all_html("data/1_bronze", "data/2_silver")

def load():
    load_all_jsons("data/2_silver", "data/3_gold")

def profile():
    run_data_profile("data/3_gold/jobs.db")

def all():
    ingest()
    print("\n")
    process()
    print("\n")
    load()
    print("\n")
    profile()

commands = {
    "ingest": ingest,
    "process": process,
    "load": load,
    "profile": profile,
    "all": all
}

def main():
    if len(sys.argv) == 2:
        commands.get(sys.argv[1], lambda: print(f"Unknown command: {sys.argv[1]}"))()
    else:
        print("Usage: python", sys.argv[0], "[ingest|process|load|profile|all]")


if __name__ == "__main__":
    main()
