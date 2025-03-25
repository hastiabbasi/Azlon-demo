import json
import os
from datetime import datetime

MEMORY_FILE = "./memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"history": []}, f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)
    
def save_memory(memory_data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_data, f, indent=4)

def get_past_response(user_prompt, test_conditions):
    memory = load_memory()
    for entry in memory["history"]:
        if entry["user_prompt"] == user_prompt and entry["test_conditions"] == test_conditions:
            return entry
        return None
    
def store_response(user_prompt, test_conditions, dockerfile, files, workflow_id):
    memory = load_memory()

    memory["history"].append({
        "user_prompt": user_prompt,
        "test_conditions": test_conditions,
        "dockerfile": dockerfile,
        "files": files,
        "workflow_id": workflow_id, 
        "timestamp": datetime.utcnow().isoformat()
    })

    save_memory(memory)