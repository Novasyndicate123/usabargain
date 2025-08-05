import os
import json
import random
from datetime import datetime

PERSONA_DIR = "data/personas"

class PersonaSimulator:
    def __init__(self, persona_names=None):
        self.persona_names = persona_names or []
        self.personas = []
        self.load_personas()

    def load_personas(self):
        self.personas = []
        for name in self.persona_names:
            filename = os.path.join(PERSONA_DIR, f"{name}.json")
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.personas.append(data)

    def simulate_conversation(self, topic, turns=3):
        dialogue = []
        if not self.personas:
            return "No personas loaded."

        for i in range(turns):
            persona = random.choice(self.personas)
            response = f"{persona['name']} ({persona['role']}): On '{topic}', I think {self.generate_opinion(persona)}"
            dialogue.append(response)
        return "\n".join(dialogue)

    def generate_opinion(self, persona):
        traits = persona.get("traits", [])
        opinions = [
            "this is critical to success.",
            "it requires more data.",
            "the user experience can be improved.",
            "the design looks solid.",
            "there are potential risks involved.",
            "it aligns with our goals."
        ]
        opinion = random.choice(opinions)
        return f"{opinion} (Traits: {traits})"

if __name__ == "__main__":
    simulator = PersonaSimulator(persona_names=["nova_critic"])
    topic = "homepage design"
    print(simulator.simulate_conversation(topic))
