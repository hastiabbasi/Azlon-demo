import json
import os

MEMORY_FILE = "memory.json"

def load_memory():

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return{}

def save_memory(memory_store):
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f, indent=4)

def update_memory(workflow_id, new_data):
    memory_store = load_memory()

    if workflow_id not in memory_store:
        memory_store[workflow_id] = {"history": []}

    if user_input:
        memory_store[workflow_id]["history"].append({"user": user_input})
    if output:
        memory_store[workflow_id]["history"].append({"output": output})
   
    return memory_store[workflow_id]