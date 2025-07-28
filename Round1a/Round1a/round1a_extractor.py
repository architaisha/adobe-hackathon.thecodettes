import fitz  # PyMuPDF

def extract_pdf_text(pdf_path="sample.pdf"):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    extracted_data = []

    # Loop through each page
    for page in doc:
        page_number = page.number + 1
        blocks = page.get_text("dict")["blocks"]

        # Extract text spans from each block
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:  # Ignore empty lines
                            extracted_data.append({
                                "text": text,
                                "font": span["font"],
                                "size": span["size"],
                                "page": page_number
                            })
    return extracted_data

# Example: Run this script directly
if __name__ == "__main__":
    data = extract_pdf_text("input/sample.pdf")
    
    # Print the first 10 items for preview
    for item in data:
        print(f"[Page {item['page']}] ({item['size']:.1f}pt {item['font']}): {item['text']}")
