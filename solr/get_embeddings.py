import sys
import json

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    return model.encode(text, convert_to_tensor=False).tolist()



if __name__ == '__main__':
    data = json.load(sys.stdin)

    for document in data:
        abstract_id = document.get("abstract_id", "")
        content = document.get("content", "")
        species = document.get("species", "")

        combined_text = str(abstract_id) + " " + content + " " + species
        document["vector"] = get_embedding(combined_text)
    
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
