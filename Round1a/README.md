Challenge 1a: PDF Processing Solution

## Overview

This project is a complete solution for Challenge 1a of the Adobe India Hackathon 2025. It implements a robust PDF processing pipeline that extracts structured section-level data from PDF documents and generates output JSON files conforming to the required schema. The system is containerized using Docker and adheres strictly to all resource, runtime, and architectural constraints.


## Official Challenge Requirements

### Submission Components

- Functional Dockerfile in root directory  
- `README.md` documenting architecture, usage, and constraints  
- Code to extract structured outlines (Title, H1, H2, H3)  
- Outputs matching Adobe's JSON schema  
- No internet access required during execution  


## Build and Run Instructions

### Build Command

```bash
docker build --no-cache --platform linux/amd64 -t pdfextractor:latest .

```

### Run Command

```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdfextractor:round1a
```

> On Windows (CMD):
> ```bash
> docker run --rm -v "%cd%\input:/app/input:ro" -v "%cd%\output:/app/output" --network none pdfextractor:round1a
> ```

## Project Structure

Round1a/
├── main.py                   # Orchestrates the pipeline (Member 3)
├── round1a_extractor.py      # PDF text + metadata extractor (Member 1)
├── round1a_classifier.py     # Heading classifier based on font/size (Member 2)
├── Dockerfile                # Docker container definition
├── requirements.txt          # Project dependencies
├── input/                    # Input PDFs (read-only)
│   └── sample.pdf
├── output/                   # Output JSONs (one per input PDF)
│   └── sample.json
└── README.md                 # This file




## Output Format

For each PDF (e.g., `sample.pdf`), the system produces `sample.json` in the following structure:

json
{
  "title": "Exploring Artificial Intelligence in Depth",
  "outline": [
    {
      "page": 1,
      "headings": [
        { "text": "Chapter 1: Introduction to AI Concepts", "level": "H1" },
        { "text": "Applications of AI", "level": "H2" },
        { "text": "Challenges in AI", "level": "H3" }
      ]
    }
  ]
}


This format is fully compatible with the schema provided in `sample_dataset/schema/output_schema.json`.


## Implementation Details

### Input Handling

- All PDFs in `/app/input/` are automatically processed.
- Only `.pdf` files are scanned; others are ignored.
- Input directory is read-only, as per spec.

### Section Extraction

- **Text blocks** are extracted using `PyMuPDF` (`fitz`) for positional and font metadata.
- **Heading levels** (`H1`, `H2`, `H3`) are inferred based on font size and position patterns.
- **Title** is detected using the largest consistent font on the first page.

### Output Generation

- Each PDF generates a single `.json` file under `/app/output/`
- Output filenames match input PDF filenames (e.g., `sample.pdf → sample.json`)


## Performance & Constraints

| Constraint                     | Status |
|--------------------------------|--------|
| Execution Time ≤ 10 sec (50pg) | Passed |
| Model size ≤ 200MB             | No models used |
| Network Disabled               | Fully offline |
| Memory ≤ 16 GB RAM             | Optimized |
| CPU (amd64, 8 cores)           | Compatible |
| Docker Containerization        | Dockerfile in root |
| Input from `/app/input:ro`     | Read-only volume |
| Output to `/app/output`        | JSON per PDF |


## Testing

### Tested Scenarios

- PDFs with single and multi-page structure
- Repeated vs. varied headings
- Cross-font and layout PDFs
- Title + H1/H2/H3 detection
- Non-destructive volume binding (input read-only)

### Sample Test Case

A multi-page test file (`sample_varied_headings.pdf`) was used to validate:
- Section hierarchy detection
- Unique outline per page
- Format compliance


## Notes

- The solution does not rely on machine learning — heading inference is based on layout heuristics, ensuring lightweight execution and fast response.
- The container is platform-specific to `linux/amd64`, as required.
- All libraries used are open source and declared in `requirements.txt`.



## Validation Checklist

- [x] All PDFs processed from `/app/input`
- [x] Output `.json` generated per `.pdf` file
- [x] Output matches required schema
- [x] Execution completes within time and memory limits
- [x] Solution runs fully offline in a Docker container
- [x] Tested on `amd64` Linux backend
