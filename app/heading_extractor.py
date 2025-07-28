def extract_heading_candidates(pages):
    heading_data = []
    for page_num, page in enumerate(pages, start=1):
        for element in page:
            if hasattr(element, "get_text"):
                text = element.get_text().strip()
                if len(text) < 150 and text and "\n" not in text:
                    font_sizes = [char.size for char in element if hasattr(char, 'size')]
                    if font_sizes:
                        avg_size = sum(font_sizes) / len(font_sizes)
                        heading_data.append({
                            "text": text,
                            "font_size": round(avg_size, 1),
                            "page": page_num
                        })
    return heading_data