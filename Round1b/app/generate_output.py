import json
import os
from datetime import datetime

def generate_output(input_dir, ranked_sections_path, output_path):
    input_json_path = os.path.join(input_dir, "input.json")

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    
    metadata = {
        "input_documents": [doc["filename"] for doc in input_data.get("documents", [])],
        "persona": input_data.get("persona", {}).get("role", ""),
        "job_to_be_done": input_data.get("job_to_be_done", {}).get("task", ""),
        "processing_timestamp": datetime.utcnow().isoformat()
    }

    with open(ranked_sections_path, "r", encoding="utf-8") as f:
        ranked = json.load(f)

    sections = []
    subsections = []

    for i, s in enumerate(ranked[:5], 1):
        sections.append({
            "document": s["document"],
            "page": s["page"],
            "section_title": s["section_title"],
            "importance_rank": i
        })
        subsections.append({
            "document": s["document"],
            "page": s["page"],
            "refined_text": s["text"]
        })

    final_json = {
        "metadata": metadata,
        "extracted_sections": sections,
        "subsection_analysis": subsections
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)

    print(f"Final output saved to {output_path}")

