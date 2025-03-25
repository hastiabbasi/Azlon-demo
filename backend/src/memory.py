import json
import os

# Path to memory.json, relative to the current file
MEMORY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../memory.json"))

def initialize_memory():
    """Ensure memory.json exists and is properly initialized."""
    if not os.path.exists(MEMORY_FILE) or os.stat(MEMORY_FILE).st_size == 0:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)  # Initialize with an empty list

def append_to_memory(entry):
    """Appends a new entry (user prompt, test conditions, output) to memory.json."""
    try:
        initialize_memory()
        
        # Load existing memory
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        # Append the new entry
        memory.append(entry)

        # Write updated memory back to the file
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
        
        print("Memory updated successfully.")
    
    except Exception as e:
        print(f"Error saving to memory: {e}")

def load_memory():
    """Loads memory.json and returns its contents."""
    initialize_memory()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

'''
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
'''