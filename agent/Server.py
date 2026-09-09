from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import time
import uuid
import json
import re
import os
# Imports the frozen compiled agent_graph from your local graph script
from agent.graph import agent_graph

app = FastAPI(title="Cred Support Agent Production Server", version="1.0.0")

# --- Task 11: Inbound Request Validation Model ---
class AskRequest(BaseModel):
    query: str = Field(description="The raw string inquiry text sent by the user client.")

# --- Task 11: Outbound Response Validation Model ---
class AskResponse(BaseModel):
    trace_id: str = Field(description="Unique tracking token generated dynamically for telemetry verification.")
    is_safe: bool
    resolved_intent: str
    response_text: str
    action_recommended: str
    execution_time_ms: float = Field(description="Total processing framework execution latency in milliseconds.")

# --- Task 12: Zero-PII Log Scrubber Engine ---
def mask_log_pii(text: str) -> str:
    """Insulates persistent disk store metrics from clear-text financial identifiers."""
    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    aadhaar_pattern = r'\b[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}\b'
    bank_account_pattern = r'\b[0-9]{9,18}\b'
    
    sanitized = re.sub(pan_pattern, "[MASKED_PAN]", text, flags=re.IGNORECASE)
    sanitized = re.sub(aadhaar_pattern, "[MASKED_AADHAAR]", sanitized)
    sanitized = re.sub(bank_account_pattern, "[MASKED_BANK_ACCOUNT]", sanitized)
    return sanitized

# --- Operational Endpoint Handlers ---
@app.get("/health")
async def health_check():
    """Simple status probe verifying that the api backend engine is alive."""
    return {"status": "healthy", "engine": "LangGraph MOCK_LLM Portfolio"}

@app.post("/ask", response_model=AskResponse)
async def ask_agent(payload: AskRequest, x_thread_id: str = Header(default="default-production-session")):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    # --- Task 15 Implementation Check: Thread ID Config Pass ---
    # This explicit configuration tells the SQLite checkpointer where to save 
    # and look up the state snapshot for this specific user session.
    config = {"configurable": {"thread_id": x_thread_id}}
    
    graph_inputs = {
        "query": payload.query, 
        "history": [],
        "retrieved_context": "",
        "application_data": None,
        "error": ""
    }
    
    try:
        # Run the inbound text query down the graph sequence with the thread configuration locked
        graph_output = agent_graph.invoke(graph_inputs, config=config)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Graph Execution Failure: {str(err)}")
        
    execution_time_ms = round((time.time() - start_time) * 1000, 2)
    
    # Extract the strict validated output dict packed by the generator_node
    final_payload = graph_output.get("final_output", {})
    if not final_payload:
        raise HTTPException(status_code=500, detail="Internal State Matrix Compilation Error.")

    # --- Task 12: High-Integrity Masked JSON-Lines Log Generation ---
    sanitized_log_query = mask_log_pii(payload.query)
    
    log_entry = {
        "trace_id": trace_id,
        "thread_id": x_thread_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "masked_input_query": sanitized_log_query,
        "resolved_intent": final_payload.get("resolved_intent"),
        "agent_response_text": final_payload.get("response_text"),
        "latency_ms": execution_time_ms
    }
    
    # Write execution records as one distinct standalone JSON line
    os.makedirs("logs", exist_ok=True)
    with open("logs/server_logs.jsonl", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")
        
    # Return structured AskResponse formatting directly to the API channel
    return AskResponse(
        trace_id=trace_id,
        is_safe=final_payload.get("is_safe", True),
        resolved_intent=final_payload.get("resolved_intent", "out_of_scope"),
        response_text=final_payload.get("response_text", ""),
        action_recommended=final_payload.get("action_recommended", "STANDARD_QUEUE"),
        execution_time_ms=execution_time_ms
    )
