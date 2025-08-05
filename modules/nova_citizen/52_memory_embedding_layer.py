import os
import json
import numpy as np
from sklearn.decomposition import PCA
from typing import List

PERSONA_DIR = "data/personas"
EMBEDDING_FILE = "data/personas/memory_embeddings.json"

def load_memories(persona_name: str) -> List[str]:
    filename = os.path.join(PERSONA_DIR, f"{persona_name}.json")
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        memories = [m["event"] for m in data.get("memory", [])]
    return memories

def embed_texts(texts: List[str]) -> np.ndarray:
    import warnings
    vectors = []
    for text in texts:
        vec = np.array([hash(word) % 1000 / 1000.0 for word in text.split()])
        vectors.append(vec)
    max_len = max(len(v) for v in vectors)
    padded = [np.pad(v, (0, max_len - len(v)), constant_values=0) for v in vectors]
    matrix = np.vstack(padded)
    
    n_samples, n_features = matrix.shape
    n_components = min(5, n_samples, n_features)
    
    if n_components == 0:
        warnings.warn("No data to embed, returning empty array.")
        return np.array([])
    
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(matrix)
    return reduced

def save_embeddings(persona_name: str, embeddings: np.ndarray):
    os.makedirs(os.path.dirname(EMBEDDING_FILE), exist_ok=True)
    embeddings_list = embeddings.tolist()
    data = {persona_name: embeddings_list}
    if os.path.exists(EMBEDDING_FILE):
        with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing.update(data)
        data = existing
    with open(EMBEDDING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    persona_name = "nova_critic"
    memories = load_memories(persona_name)
    if not memories:
        print(f"No memories found for {persona_name}")
    else:
        embeddings = embed_texts(memories)
        save_embeddings(persona_name, embeddings)
        print(f"Saved {len(embeddings)} embeddings for {persona_name}")
