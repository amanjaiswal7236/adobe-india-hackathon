from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

from .config import MAX_PAGES

def extract_text_blocks(pdf_path):
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

def extract_title(blocks):
    first_page = [b for b in blocks if b["page"] == 0]
    if not first_page:
        return "Untitled Document"
    return max(first_page, key=lambda b: b["size"])["text"]
