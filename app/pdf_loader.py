from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar

def load_pdf_layout(filepath):
    pages = list(extract_pages(filepath))
    return pages

def extract_font_info(text_container):
    fonts = set()
    for obj in text_container:
        if isinstance(obj, LTChar):
            fonts.add((obj.fontname, round(obj.size, 1)))
    return fonts