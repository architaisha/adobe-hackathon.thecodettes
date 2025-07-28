
##  Adobe Hackathon 2025 — Round 1B: Connecting the Dots

##  Overview

This project is the solution for **Round 1B** of Adobe’s "Connecting the Dots" Hackathon.  
The goal is to extract, rank, and structure key sections from a collection of diverse PDF documents, tailored to a given **persona** and **job-to-be-done**.

>  Documents can be from varied domains like research papers, travel guides, financial reports, or school textbooks.  
>  Personas and  Jobs are automatically inferred from document content (for 4 known test cases), ensuring a **generalized and automated pipeline**.



##  Project Structure

```
.
├── app/
│   ├── main.py
│   ├── extract_sections.py
│   ├── rank_sections.py
│   ├── generate_output.py
│   ├── config.json
│   └── requirements.txt
├── input/               # Place your input PDFs here
│   └── input.json       # (Optional) Will be auto-generated if missing
├── output/              # Final outputs go here
│   └── final_output.json
├── Dockerfile
└── README.md            # You’re here!
```



##  Supported Sample Test Cases

| Test Case           | Auto Detected From Filename Includes         | Persona                          | Job to be Done |
|---------------------|-----------------------------------------------|----------------------------------|----------------|
| `menu_planning`      | _(default fallback)_                         | Food Contractor                  | Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items. |
| `academic_research`  | `"graph"`, `"drug"`                          | PhD Researcher in Computational Biology | Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks. |
| `business_analysis`  | `"financial"`, `"annual report"`             | Financial Analyst                | Summarize key financial insights from annual reports of major corporations. |
| `travel_guide`       | `"south of france"`, `"travel"`, `"cuisine"` | Travel Guide Curator             | Design a cultural and culinary travel experience in the South of France for premium clients. |



##  Core Pipeline

1. **Extract Sections**: PDF content is parsed into structured sections with titles and pages.
2. **Auto-generate `input.json`**: If not provided, it's generated based on PDF filenames + `config.json`.
3. **Infer Persona & Job**: Matched from config using smart PDF name detection.
4. **Rank Sections**: Sections are ranked based on relevance to the persona and job using sentence embeddings.
5. **Generate Output**: Final structured JSON is created with metadata, top sections, and summaries.



##  How to Run

###  With Docker (Recommended)

>  Make sure Docker is installed and running.

1. **Build the Docker image:**
   ```bash
   docker build -t adobe-b-ranker .
   ```

2. **Run the container:**
   ```bash
   docker run -v "%cd%\input":/app/input -v "%cd%\output":/app/output adobe-b-ranker
   ```

   >  This will:
   > - Extract sections
   > - Auto-generate `input.json` (if missing)
   > - Infer persona & job from PDF names
   > - Rank relevant sections
   > - Save final JSON to `output/final_output.json`



##  Development Mode (Manual Python)

> Requires Python 3.10+, pip, and poppler (for PDF processing)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the pipeline:**
   ```bash
   python main.py
   ```



##  config.json Format

```
{
  "menu_planning": {
    "persona": "Food Contractor",
    "job_to_be_done": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
  },
  "academic_research": {
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks."
  },
  "business_analysis": {
    "persona": "Financial Analyst",
    "job_to_be_done": "Summarize key financial insights from annual reports of major corporations."
  },
  "travel_guide": {
    "persona": "Travel Guide Curator",
    "job_to_be_done": "Design a cultural and culinary travel experience in the South of France for premium clients."
  }
}
```



##  Sample Output (final_output.json)

```
{
  "metadata": {
    "input_documents": ["South of France - Cuisine.pdf", "..."],
    "persona": "Travel Guide Curator",
    "job_to_be_done": "Design a cultural and culinary travel experience in the South of France for premium clients.",
    "processing_timestamp": "2025-07-28T12:52:16.071105"
  },
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
```



##  Notes

- If `input/input.json` is already present, the code updates its persona and job using PDF analysis.
- Supports multiple PDF inputs.
- You do **not** need to call HuggingFace or external APIs. It works locally with SentenceTransformers.
- Code is modular and extendable for additional test cases.



##  Future Work

- Dynamic persona/job inference via LLMs or Adobe APIs (if allowed)
- GUI to upload PDFs and preview outputs
- Scoring logic for ranked sections



>  "Connect the dots between documents and decisions." — Adobe Hackathon 2025
