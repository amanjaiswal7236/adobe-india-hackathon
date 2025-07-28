from app.pdf_loader import load_pdf_layout
from app.title_extractor import extract_title
from app.heading_extractor import extract_heading_candidates
from app.heading_clustering import cluster_headings
from app.json_generator import generate_output_json

import os

def process_pdf(filepath, output_dir):
    pages = load_pdf_layout(filepath)
    title = extract_title(pages)
    headings = extract_heading_candidates(pages)
    clustered = cluster_headings(headings)
    filename = os.path.splitext(os.path.basename(filepath))[0] + ".json"
    generate_output_json(title, clustered, os.path.join(output_dir, filename))