import json
import os
from datetime import datetime

PERSONA_DIR = "data/personas"

class Persona:
    def __init__(self, name, role, traits=None, memory=None):
        self.name = name
        self.role = role
        self.traits = traits or []
        self.memory = memory or []

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "traits": self.traits,
            "memory": self.memory
        }

    def save(self):
        os.makedirs(PERSONA_DIR, exist_ok=True)
        filename = os.path.join(PERSONA_DIR, f"{self.name.lower().replace(' ', '_')}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        return filename

    def remember(self, event):
        timestamp = datetime.utcnow().isoformat()
        self.memory.append({"timestamp": timestamp, "event": event})
        self.save()

    def speak(self, prompt):
        response = f"{self.name} ({self.role}): I believe '{prompt}' deserves a thoughtful answer based on {self.traits}."
        self.remember(f"Responded to prompt: {prompt}")
        return response


# === Sample Initialization ===
if __name__ == "__main__":
    nova_test = Persona(
        name="Nova Critic",
        role="Product Reviewer",
        traits=["analytical", "blunt", "customer-focused"]
    )
    nova_test.remember("Observed prototype module failure.")
    print(nova_test.speak("What do you think of the homepage design?"))
