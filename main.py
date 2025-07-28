import os
import json
from pathlib import Path
from collections import defaultdict

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

from sklearn.cluster import DBSCAN
import numpy as np


# === CONFIGURATION === #
MAX_PAGES = 50
HEADING_LEVELS = 3
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_blocks(pdf_path):
    """
    Extracts text blocks with font size and bold metadata from a PDF.
    """
    blocks = []
    for page_num, layout in enumerate(extract_pages(pdf_path)):
        if page_num >= MAX_PAGES:
            break
        for element in layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    text = line.get_text().strip()
                    if not text:
                        continue
                    font_sizes = []
                    is_bold = False
                    for char in line:
                        if isinstance(char, LTChar):
                            font_sizes.append(char.size)
                            if "Bold" in char.fontname or "bold" in char.fontname:
                                is_bold = True
                    if font_sizes:
                        avg_size = sum(font_sizes) / len(font_sizes)
                        blocks.append({
                            "text": text,
                            "size": avg_size,
                            "bold": is_bold,
                            "page": page_num,
                            "y0": line.y0
                        })
    return blocks


def cluster_headings(blocks):
    """
    Uses font size and vertical position clustering to identify headings.
    """
    headings = []
    blocks_by_page = defaultdict(list)
    for b in blocks:
        blocks_by_page[b["page"]].append(b)

    for page, page_blocks in blocks_by_page.items():
        candidates = [b for b in page_blocks if b["size"] > 8]
        if not candidates:
            continue

        y_coords = np.array([[b["y0"]] for b in candidates])
        clustering = DBSCAN(eps=15, min_samples=1).fit(y_coords)

        clusters = defaultdict(list)
        for idx, label in enumerate(clustering.labels_):
            clusters[label].append(candidates[idx])

        top_lines = []
        for cluster_blocks in clusters.values():
            cluster_blocks.sort(key=lambda b: (-b["size"], not b["bold"]))
            top_lines.append(cluster_blocks[0])

        unique_sizes = sorted(set(b["size"] for b in top_lines), reverse=True)
        level_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes[:HEADING_LEVELS])}

        for b in top_lines:
            level = level_map.get(b["size"])
            if level:
                headings.append({
                    "level": level,
                    "text": b["text"],
                    "page": b["page"] + 1
                })
    return headings


def extract_title(blocks):
    """
    Picks the largest text from the first page as the document title.
    """
    first_page = [b for b in blocks if b["page"] == 0]
    if not first_page:
        return "Untitled Document"
    return max(first_page, key=lambda b: b["size"])["text"]


def process_pdf(pdf_path: Path):
    """
    Full processing of a single PDF: text block extraction, heading clustering, JSON export.
    """
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
    """
    Run heading extraction for all PDFs in the input directory.
    """
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {INPUT_DIR.resolve()}")
        return

    for pdf_path in pdf_files:
        process_pdf(pdf_path)

    print(f"\n✅ All files processed. JSONs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    run_batch_heading_extraction()