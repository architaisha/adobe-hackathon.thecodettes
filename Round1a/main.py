import os
from round1a_extractor import extract_pdf_text
from round1a_classifier import detect_title, detect_headings, save_output

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
OUTPUT_FILE = "output.json"

def main():
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".pdf")]
    if not files:
        print("No PDF file found in the input folder.")
        return

    pdf_path = os.path.join(INPUT_FOLDER, files[0])
    print(f"Processing file: {pdf_path}")

    extracted_data = extract_pdf_text(pdf_path)
    title = detect_title(extracted_data)
    outline = detect_headings(extracted_data)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    save_output(title, outline, output_path)

if __name__ == "__main__":
    main()
