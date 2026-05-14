from pathlib import Path
from email import message_from_binary_file
import quopri
import logging

def ingest_all_mhtml(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    if not input_dir.is_dir():
        logging.error(f"Failed to ingest: {input_dir}/ | Reason: {input_dir}/ not found")
        return

    total = 0
    success = 0
    fail = 0
    print("🥉 Bronze:...")
    for f in input_dir.iterdir():
        if f.is_file() and f.suffix == ".mhtml":
            total += 1
            if ingest_mhtml(f, output_dir):
                success += 1
            else:
                fail += 1
    print("\n📊 Bronze Summary:\nTotal:", total, "| Extracted:", success, "| Failed:", fail)

def ingest_mhtml(infile, output_dir):
    outfile = output_dir / (infile.stem + ".html")

    mhtml_data = message_from_binary_file(infile.open("rb"))
    for part in mhtml_data.walk():
        if part.get_content_type() == "text/html":
            outfile.write_text(quopri.decodestring(part.get_payload(decode=False)).decode())
            logging.info(f"✅ Extracted: {infile.name}")
            return True
    logging.warning(f"⚠️ No HTML content found in: {infile.name}")
    return False