import threading
import time
import random

class Agent(threading.Thread):
    def __init__(self, name, behavior_func):
        super().__init__()
        self.name = name
        self.behavior_func = behavior_func
        self.running = True

    def run(self):
        while self.running:
            result = self.behavior_func(self.name)
            print(f"[{self.name}] {result}")
            time.sleep(random.uniform(1, 3))

    def stop(self):
        self.running = False

def sample_behavior(agent_name):
    actions = [
        "scanning market trends",
        "optimizing affiliate links",
        "curating deals",
        "monitoring competitor prices",
        "analyzing user engagement"
    ]
    return random.choice(actions)

if __name__ == "__main__":
    agents = []
    for i in range(5):
        agent = Agent(f"Agent-{i+1}", sample_behavior)
        agent.start()
        agents.append(agent)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping agents...")
        for agent in agents:
            agent.stop()
        for agent in agents:
            agent.join()
        print("All agents stopped.")
