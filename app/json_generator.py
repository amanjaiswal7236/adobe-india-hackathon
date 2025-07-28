import json

def generate_output_json(title, headings, output_path):
    headings_out = [
        {"level": h["level"], "text": h["text"], "page": h["page"]}
        for h in sorted(headings, key=lambda x: (x['page'], -x['font_size']))
    ]
    result = {
        "title": title,
        "outline": headings_out
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)