import os
import json

# Always resolve the memory file relative to this file's location
memory_file_path = os.path.join(os.path.dirname(__file__), "memory.json")

# Ensure the memory file exists
if not os.path.exists(memory_file_path):
    with open(memory_file_path, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_memory():
    with open(memory_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    try:
        with open(memory_file_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
        print("✅ memory.json written successfully.")
    except Exception as e:
        print(f"❌ Error writing memory.json: {e}")

def append_to_memory(entry):
    print("[append_to_memory] called")
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)

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
            entry.get("user_prompt") == user_prompt and
            entry.get("test_conditions") == test_conditions
        ):
            return entry
    return None
