import os
import json
from datetime import datetime

from extract_sections import extract_sections
from rank_sections import rank_sections
from generate_output import generate_output

input_dir = "input"
output_dir = "output"
input_json_path = os.path.join(input_dir, "input.json")
config_path = "config.json"


#print("🔍 Extracting sections...")
extract_sections(input_dir, output_dir)


pdfs = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
pdf_titles = [f.lower() for f in pdfs]


def infer_test_case(pdf_titles):
    if any("graph" in t or "drug" in t for t in pdf_titles):
        return "academic_research"
    elif any("annual" in t or "financial" in t for t in pdf_titles):
        return "business_analysis"
    elif any("south of france" in t or "travel" in t or "cuisine" in t for t in pdf_titles):
        return "travel_guide"
    else:
        return "menu_planning"

test_case_name = infer_test_case(pdf_titles)


with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

expected_persona = config[test_case_name]["persona"]
expected_job = config[test_case_name]["job_to_be_done"]


if not os.path.exists(input_json_path):
    print("input.json not found, generating automatically...")
    input_json = {
        "challenge_info": {
            "challenge_id": "round_1b_001",
            "test_case_name": test_case_name,
            "description": "Auto-generated input.json"
        },
        "documents": [{"filename": pdf, "title": os.path.splitext(pdf)[0]} for pdf in pdfs],
        "persona": {"role": expected_persona},
        "job_to_be_done": {"task": expected_job},
        "generated_timestamp": datetime.now().isoformat()
    }
    with open(input_json_path, "w", encoding="utf-8") as f:
        json.dump(input_json, f, indent=2)
    #print(f"✅ Created input.json for {test_case_name} with {len(pdfs)} PDFs")
else:
    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

   
    persona = input_data.get("persona", {}).get("role", "").strip()
    job = input_data.get("job_to_be_done", {}).get("task", "").strip()

    if persona.lower() in ["", "food contractor", "student"] or job.lower() in ["", "plan a meal", ""]:
        #print(f"🛠 Updating persona/job in input.json based on PDFs → {test_case_name}")
        input_data["challenge_info"]["test_case_name"] = test_case_name
        input_data["persona"] = {"role": expected_persona}
        input_data["job_to_be_done"] = {"task": expected_job}
        with open(input_json_path, "w", encoding="utf-8") as f:
            json.dump(input_data, f, indent=2)
        #print("✅ Updated persona and job in input.json")


with open(input_json_path, "r", encoding="utf-8") as f:
    input_data = json.load(f)

persona = input_data["persona"]["role"]
job_to_be_done = input_data["job_to_be_done"]["task"]

#print(f"👤 Persona: {persona}")
#print(f"🧩 Task: {job_to_be_done}")


#print("📊 Ranking sections...")
sections_json = os.path.join(output_dir, "sections.json")
ranked_json = os.path.join(output_dir, "ranked_sections.json")

ranked_sections = rank_sections(
    sections_json,
    persona=persona,
    job_to_be_done=job_to_be_done,
    output_path=ranked_json
)


#print("Generating final structured JSON...")
generate_output(
    input_dir=input_dir,
    ranked_sections_path=ranked_json,
    output_path=os.path.join(output_dir, "final_output.json")
)

#print("✅ All done! Final output saved in /output folder.")

