def extract_title(pages):
    if not pages:
        return ""
    title_candidates = []
    for element in pages[0]:
        if hasattr(element, "get_text"):
            text = element.get_text().strip()
            if text:
                size = max((char.size for char in element if hasattr(char, 'size')), default=0)
                title_candidates.append((text, size))
    title_candidates.sort(key=lambda x: -x[1])
    return title_candidates[0][0] if title_candidates else ""