from pathlib import Path
from bs4 import BeautifulSoup
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

class JobListing(BaseModel):
    source_id: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    company: str = Field(min_length=1)
    description: str = Field(min_length=1)

def process_all_html(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    if not input_dir.is_dir():
        print(input_dir, "/ path not found", sep="")
        return
    
    total = 0
    success = 0
    fail = 0
    print("🥈 Silver: ", output_dir, "/", sep="")
    for f in input_dir.iterdir():
        if f.is_file() and f.suffix == ".html":
            total += 1
            if process_html(f, output_dir):
                success += 1
            else:
                fail += 1
    print("\n📊 Silver Summary:\nTotal:", total, "| Processed:", success, "| Skipped:", fail)

def process_html(infile, output_dir):
    outfile = output_dir / (infile.stem + ".json")

    soup = BeautifulSoup(infile.read_text(encoding="utf-8"), "html.parser")

    source_id = get_value_from_soup(soup, attribute="content", attrs={"property": "og:url"})
    job_title = get_value_from_soup(soup, attrs={"data-automation": "job-detail-title"})
    company = get_value_from_soup(soup, attrs={"data-automation": "advertiser-name"})
    description = get_value_from_soup(soup, attrs={"data-automation": "jobAdDetails"})

    source_id = Path(source_id).name

    try:
        job = JobListing(
            source_id=source_id,
            job_title=job_title,
            company=company,
            description=description
        )
        outfile.write_text(job.model_dump_json(indent=4))
        print("✅ Processed:", infile.name)
        return True
    except ValidationError as e:
        for error in e.errors():
            loc = error['loc'][0].strip("('')")
            print("⚠️ Missing", loc, "in:", infile.name)
        return False

def get_value_from_soup(soup, attribute=None, **kwargs):
    value = soup.find(**kwargs)
    if value:
        if attribute:
            value = value.get(attribute)
        else:
            value = value.get_text(separator=" ", strip=True)
    return value