import json
from sentence_transformers import SentenceTransformer, util

def rank_sections(sections_path, *, persona, job_to_be_done, output_path):
    from sentence_transformers import SentenceTransformer, util
    import json

    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open(sections_path, "r", encoding="utf-8") as f:
        sections = json.load(f)

    query_embedding = model.encode(persona + " " + job_to_be_done, convert_to_tensor=True)

    ranked = []
    for section in sections:
        section_embedding = model.encode(section["text"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, section_embedding).item()
        ranked.append({**section, "score": score})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    top5 = ranked[:5]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(top5, f, indent=2)
    print(f"Ranked sections saved to {output_path}")

    return top5

