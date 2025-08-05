import json
import os
import random

EMBEDDING_FILE = "data/personas/memory_embeddings.json"

class ReactionEngine:
    def __init__(self):
        self.embeddings = {}
        self.load_embeddings()

    def load_embeddings(self):
        if os.path.exists(EMBEDDING_FILE):
            with open(EMBEDDING_FILE, "r", encoding="utf-8") as f:
                self.embeddings = json.load(f)

    def evaluate_response(self, persona_name, response):
        # Simple heuristic-based scoring
        score = 0
        score += len(response.split()) / 10  # Longer responses get some points
        if "critical" in response.lower():
            score += 2
        if "improved" in response.lower():
            score += 1.5
        if persona_name in self.embeddings:
            score += 1  # Bonus if embeddings exist for persona

        feedback = "Positive" if score > 3 else "Neutral"
        return score, feedback

if __name__ == "__main__":
    engine = ReactionEngine()
    test_persona = "nova_critic"
    test_response = "The homepage design requires more data and user feedback."
    score, feedback = engine.evaluate_response(test_persona, test_response)
    print(f"Score: {score}, Feedback: {feedback}")
