# ./backend/main.py

from fastapi import FastAPI, HTTPException, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from pydantic import BaseModel # type: ignore
import time
import os

from src.client import client
from src.prompts import get_prompts, set_prompts
from restack_ai import Restack # type: ignore

from memory import load_memory, save_memory, update_memory

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class UserInput(BaseModel):
    user_prompt: str
    test_conditions: str
    human_feedback: str = None
    # added workflow_id for human-in-loop processing
    workflow_id: str = None 

class PromptsInput(BaseModel):
    generate_code_prompt: str
    validate_output_prompt: str

@app.get("/prompts")
def fetch_prompts():
    return get_prompts()

@app.post("/prompts")
def update_prompts(prompts: PromptsInput):
    set_prompts(prompts.generate_code_prompt, prompts.validate_output_prompt)
    return {"status": "updated"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error."},
        headers={"Access-Control-Allow-Origin": "http://localhost:8080"},
    )

@app.post("/run_workflow")
async def run_workflow(params: UserInput):
    try:
        workflow_id = f"{int(time.time() * 1000)}-AutonomousCodingWorkflow"
        runId = await client.schedule_workflow(
            workflow_name="AutonomousCodingWorkflow",
            workflow_id=workflow_id,
            input=params.model_dump()
        )
        result = await client.get_workflow_result(workflow_id=workflow_id, run_id=runId)

        update_memory(workflow_id, user_input=params.user_prompt, output=result)
        return {"workflow_id": workflow_id, "result": result}
    except Exception as e:
        # If engine connection or workflow run fails, a 500 error is raised
        # The global_exception_handler ensures CORS headers are included.
        raise HTTPException(status_code=500, detail="Failed to connect to Restack engine or run workflow.")

@app.post("/human_in_loop")
async def human_in_loop(params: UserInput):
    
    try:
        if not params.worfklow_id:
            raise HTTPException(status_code=400, detail="Workflow ID required for human-in-loop feedback.")
        
        if params.human_feedback:
            params.user_prompt = apply_human_feedback(params.user_prompt, params.human_feedback)

        runID = await client.continue_workflow(
            workflow_id = params.workflow_id,
            input = params.model_dump()
        )

        result = await client.get_workflow_result(workflow_id=params.workflow_id, run_id=runID)

        memory_context = update_memory("params.workflow_id, user_input=params.user_prompt, output=rusult")

        return {"workflow_id": params.workflow_id, "result": result}
    
    except Exception as e:
        return {"error": f"Failed to process human-in-the-loop feedback: {str(e)}"}
    
def apply_human_feedback(user_prompt: str, feedback: str) -> str:

    modified_prompt = f"{user_prompt}\n # Feedback: {feedback}"

    return modified_prompt