import fitz  # pymupdf
import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ----------- Step 1: Extract PDF Text with Metadata -------------
def extract_pdf_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        all_text.append({
                            "text": span["text"].strip(),
                            "size": span["size"],
                            "font": span["font"],
                            "page": page.number + 1
                        })
    return all_text

# ----------- Step 2: Detect Title -------------
def detect_title(all_text):
    page1 = [t for t in all_text if t["page"] == 1 and t["text"]]
    return max(page1, key=lambda x: x["size"])["text"] if page1 else "Untitled Document"

# ----------- Step 3: Detect Headings -------------
def detect_headings(all_text, h1_size=20, h2_size=16, h3_size=14):
    outline = []
    for line in all_text:
        size = line["size"]
        if size >= h1_size:
            level = "H1"
        elif size >= h2_size:
            level = "H2"
        elif size >= h3_size:
            level = "H3"
        else:
            continue
        outline.append({
            "level": level,
            "text": line["text"],
            "page": line["page"]
        })
    return outline

# ----------- Step 4: Save JSON Output -------------
def save_output(title, outline, output_path):
    data = {
        "title": title,
        "outline": outline
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Output saved to {output_path}")

# ----------- Main Entry Point -------------
# ----------- Main Entry Point -------------
if __name__ == "__main__":
    input_pdf = "input/sample.pdf"
    output_json = "output/output.json"

    print(f"📄 Extracting text from: {input_pdf}")
    extracted_data = extract_pdf_blocks(input_pdf)

    print(f"🏷️  Detecting title...")
    sample_title = detect_title(extracted_data)

    print(f"🧠 Generating outline based on font size...")
    sample_outline = detect_headings(extracted_data)

    save_output(sample_title, sample_outline, output_json)
