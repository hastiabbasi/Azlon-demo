import os
import json
import io

# Absolute path to the memory file
memory_file_path = "memory.json"

# Ensure the memory file exists
if not os.path.exists(memory_file_path):
    with open(memory_file_path, "w") as f:
        json.dump([], f)

def load_memory():
    """Load memory.json as a Python list"""
    with open(memory_file_path, "r") as f:
        return json.load(f)

def save_memory(memory):
    """Write the full memory list to memory.json using BufferedWriter"""
    try:
        with open(memory_file_path, "wb") as raw_file:
            with io.BufferedWriter(raw_file) as buffered_file:
                json_str = json.dumps(memory, indent=2)
                buffered_file.write(json_str.encode("utf-8"))
                buffered_file.flush()
        print("✅ memory.json written successfully via BufferedWriter.")
    except Exception as e:
        print(f"❌ Error writing memory.json: {e}")

def append_to_memory(entry):
    """Append an entry to memory.json"""
    print("[append_to_memory] Called")
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)

def store_response(user_prompt, test_conditions, dockerfile, files, workflow_id):
    """Store a full response in memory"""
    entry = {
        "user_prompt": user_prompt,
        "test_conditions": test_conditions,
        "dockerfile": dockerfile,
        "files": files,
        "workflow_id": workflow_id
    }
    append_to_memory(entry)

def get_past_response(user_prompt, test_conditions):
    """Search memory.json for a matching past response"""
    memory = load_memory()
    for entry in memory:
        if (
            entry["user_prompt"] == user_prompt
            and entry["test_conditions"] == test_conditions
        ):
            return entry
    return None

'''
# ./backend/src/memory.py
import os
import json

# Path to the memory file
# memory_file_path = os.path.join(os.path.dirname(__file__), "memory.json")
memory_file_path = "/app/src/memory.json"

# Ensure the memory file exists
if not os.path.exists(memory_file_path):
    with open(memory_file_path, "w") as f:
        json.dump([], f)

def load_memory():
    with open(memory_file_path, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(memory_file_path, "w") as f:
        json.dump(memory, f, indent=2)

def append_to_memory(entry):
    print("append_to_memory called!")
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)

    try:
        with open(memory_file_path, "w") as f:
            json.dump(memory, f, indent=2)
        print("✅ memory.json written successfully.")
    except Exception as e:
        print(f"❌ Error writing memory.json: {e}")


def store_response(user_prompt, test_conditions, dockerfile, files, workflow_id):
    entry = {
        "user_prompt": user_prompt,
        "test_conditions": test_conditions,
        "dockerfile": dockerfile,
        "files": files,
        "workflow_id": workflow_id
    }
    append_to_memory(entry)

def get_past_response(user_prompt, test_conditions):
    memory = load_memory()
    for entry in memory:
        if (
            entry["user_prompt"] == user_prompt
            and entry["test_conditions"] == test_conditions
        ):
            return entry
    return None

'''

'''
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

############

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

'''
if __name__ == "__main__":
    test_entry = {
        "user_prompt": "What is 2 + 2?",
        "test_conditions": "Expect output to be 4",
        "generated_code": {
            "dockerfile": "FROM python:3.9",
            "files": [{"filename": "main.py", "content": "print(2 + 2)"}]
        }
    }

    append_to_memory(test_entry)

    print("✅ Test entry written! Current memory content:")
    print(json.dumps(load_memory(), indent=2))
'''