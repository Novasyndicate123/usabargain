import os
import json
import random

MARKET_STATE_FILE = "market_state.json"

class AIMarketSimulator:
    def __init__(self, personas):
        self.personas = personas
        self.market_state = {}
        self.load_market_state()

    def load_market_state(self):
        def get_persona_name(p):
            for key in ['name', 'id', 'username', 'persona', 'title']:
                if key in p:
                    return p[key]
            return f"persona_{random.randint(1000, 9999)}"

        if os.path.exists(MARKET_STATE_FILE):
            with open(MARKET_STATE_FILE, "r", encoding="utf-8") as f:
                self.market_state = json.load(f)
        else:
            self.market_state = {get_persona_name(p): {'influence': random.uniform(0, 1)} for p in self.personas}
            self.save_market_state()

    def save_market_state(self):
        with open(MARKET_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.market_state, f, indent=4)

    def simulate_market(self):
        # Simple example: influence fluctuates randomly
        for persona_name in self.market_state:
            delta = random.uniform(-0.05, 0.05)
            self.market_state[persona_name]['influence'] = max(0, min(1, self.market_state[persona_name]['influence'] + delta))
        self.save_market_state()

if __name__ == "__main__":
    # Load personas from JSON files in ./data/personas/
    import glob
    persona_files = glob.glob(os.path.join("data", "personas", "*.json"))
    personas = []
    for pf in persona_files:
        with open(pf, "r", encoding="utf-8") as f:
            try:
                personas.append(json.load(f))
            except Exception as e:
                print(f"Failed to load {pf}: {e}")

    market = AIMarketSimulator(personas)
    market.simulate_market()
    print("Market simulation step complete.")
