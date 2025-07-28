import fitz
import os
import json

def extract_sections(input_dir="input", output_dir="output"):
    output_path = os.path.join(output_dir, "sections.json")
    os.makedirs(output_dir, exist_ok=True)

    all_pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    sections = []

    for pdf_file in all_pdf_files:
        doc_path = os.path.join(input_dir, pdf_file)
        doc = fitz.open(doc_path)

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            current_section = None

            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    line_text = ""
                    max_font_size = 0

                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        line_text += text + " "
                        max_font_size = max(max_font_size, span["size"])

                    line_text = line_text.strip()
                    if not line_text:
                        continue

                    
                    if (
                        max_font_size >= 12.0
                        and len(line_text.split()) <= 5
                        and not line_text.lower().startswith("instructions")
                        and not line_text.endswith(".")
                    ):
                        if current_section and current_section["text"].strip():
                            sections.append(current_section)
                        current_section = {
                            "document": pdf_file,
                            "page": page_num,
                            "section_title": line_text,
                            "text": ""
                        }
                    elif current_section:
                        current_section["text"] += line_text + " "

            if current_section and len(current_section["text"].split()) > 10:
                sections.append(current_section)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    #print(f"Extracted {len(sections)} sections → {output_path}")

if __name__ == "__main__":
    extract_sections()

