import fitz  

def extract_pdf_text(pdf_path="sample.pdf"):
    
    doc = fitz.open(pdf_path)
    extracted_data = []

    
    for page in doc:
        page_number = page.number + 1
        blocks = page.get_text("dict")["blocks"]

        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text: 
                            extracted_data.append({
                                "text": text,
                                "font": span["font"],
                                "size": span["size"],
                                "page": page_number
                            })
    return extracted_data


if __name__ == "__main__":
    data = extract_pdf_text("input/sample.pdf")
    
    
    for item in data:
        print(f"[Page {item['page']}] ({item['size']:.1f}pt {item['font']}): {item['text']}")
