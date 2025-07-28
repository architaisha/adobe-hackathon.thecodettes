## Adobe India Hackathon 2025 — Connecting the Dots 

Welcome to our submission for Adobe’s **Connecting the Dots** challenge — a reimagination of how we read, explore, and extract knowledge from PDFs.



##  Challenge Overview

In a world full of unstructured documents, Adobe challenges us to **rethink the humble PDF** — turning static pages into dynamic, intelligent companions that understand context, highlight key insights, and adapt to diverse readers.



##  Round 1A: PDF Structure Extraction

>  `round1a/` — The foundation: fast, accurate PDF parsing & outline detection.

### Features:
- Extract Title, H1, H2, H3 sections with page numbers.
- Works on multi-page PDFs with variable formatting.
- Outputs structured `output.json` for further use.
- Packaged as a Docker container (`Dockerfile` included).



##  Round 1B: Persona-Based Document Ranking

>  `round1b/` — Deep analysis for *who* is reading and *why*.

### Pipeline Highlights:
- Accepts 3–10 PDF documents.
- Automatically infers **persona** and **job-to-be-done** based on filenames or user config.
- Extracts and ranks relevant sections using **semantic embeddings** (MiniLM) + scoring.
- Outputs a structured `final_output.json` with:
  - Metadata (persona, job)
  - Top-ranked sections and content highlights



##  Folder Structure

```
project-root/
├── round1a/
│   ├── app/
│   ├── Dockerfile
│   └── output.json
├── round1b/
│   ├── app/
│   │   ├── main.py
│   │   ├── extract_sections.py
│   │   ├── rank_sections.py
│   │   └── generate_output.py
│   ├── Dockerfile
│   ├── config.json
│   ├── input/
│   │   └── *.pdf
│   └── output/
│       ├── sections.json
│       ├── ranked_sections.json
│       └── final_output.json
```



## How to Run (Round 1B)

###  Docker (Recommended)

```bash
docker build -t adobe-b-ranker:latest .
docker run -v "%cd%/input":/app/input -v "%cd%/output":/app/output adobe-b-ranker:latest
```

###  Python (Dev Mode)

```bash
pip install -r requirements.txt
python main.py
```


## How Persona & Job Are Inferred

- **Auto-matching logic** maps filenames to known test cases (`academic_research`, `travel_guide`, etc).
- For unknown files, default fallback to `menu_planning`.
- Mappings defined in `config.json`:

```json
{
  "academic_research": {
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
  },
  "travel_guide": {
    "persona": "Food Contractor",
    "job_to_be_done": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
  }
}
```


## Sample Output (`final_output.json`)

```json
{
  "metadata": {
    "persona": "PhD Researcher in Computational Biology",
    "job_to_be_done": "Prepare a comprehensive literature review...",
    "input_documents": [...]
  },
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
```


Let’s read between the lines. Let’s **connect the dots.**
