import sys
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
from src.loader import load_all_jsons

def ingest():
    ingest_all_mhtml("data/0_source", "data/1_bronze")

def process():
    process_all_html("data/1_bronze", "data/2_silver")

def load():
    load_all_jsons("data/2_silver", "data/3_gold")

commands = {
    "ingest": ingest,
    "process": process,
    "load": load
}

def main():
    if len(sys.argv) == 2:
        commands.get(sys.argv[1], lambda: print("Unknown command"))()
    else:
        print("Usage:", sys.argv[0], "<command>")


if __name__ == "__main__":
    main()
