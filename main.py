import sys
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html

def ingest():
    ingest_all_mhtml("data/0_source", "data/1_bronze")

def process():
    process_all_html("data/1_bronze", "data/2_silver")

commands = {
    "ingest": ingest,
    "process": process
}

def main():
    if len(sys.argv) == 2:
        commands.get(sys.argv[1], lambda: print("Unknown command"))()
    else:
        print("Usage:", sys.argv[0], "<command>")


if __name__ == "__main__":
    main()
