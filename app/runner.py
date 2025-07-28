import json
from .config import INPUT_DIR, OUTPUT_DIR
from .extract import extract_text_blocks, extract_title
from .cluster import cluster_headings

def process_pdf(pdf_path):
    print(f"Processing: {pdf_path.name}")
    blocks = extract_text_blocks(pdf_path)
    title = extract_title(blocks)
    outline = cluster_headings(blocks)

    output = {
        "title": title,
        "outline": outline
    }

    output_path = OUTPUT_DIR / (pdf_path.stem + ".json")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")

def run_batch_heading_extraction():
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {INPUT_DIR.resolve()}")
        return

    for pdf_path in pdf_files:
        process_pdf(pdf_path)

    print(f"\nAll files processed. JSONs saved to: {OUTPUT_DIR.resolve()}")
