from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from loggingCentral import logger as log
import re
import csv
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# --- Task 9: Structured Output Validation Schema ---
class CredAgentResponse(BaseModel):
    is_safe: bool = Field(description="Indicates whether the input bypassed structural guardrail restrictions safely.")
    resolved_intent: str = Field(description="The final classification trajectory computed by the system router.")
    response_text: str = Field(description="The finalized string answer compiled for user presentation.")
    action_recommended: str = Field(description="Operations protocol routing tag for internal system handling.")

# --- LangGraph Core State Engine ---
class CredAgentState(TypedDict):
    query: str
    sanitized_query: str
    intent: str
    retrieved_context: str
    application_data: Optional[Dict[str, Any]]
    final_output: Dict[str, Any]
    history: List[Dict[str, str]]
    error: str

# --- Node 1: Input-Side Security Guardrail Node ---
def guardrail_node(state: CredAgentState) -> Dict[str, Any]:
    log.info(f"--- Entering Node: [{guardrail_node.__name__}] ---")
    log.info(" --- Guardrail Checking & Integrity Verification ---")
    
    raw_query = state["query"]
    
    # Structural financial formatting identification matrices (Task 10)
    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    aadhaar_pattern = r'\b[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}\b'
    bank_account_pattern = r'\b[0-9]{9,18}\b'
    
    # Linearly mask discrete localized signatures to insulate personal metrics
    sanitized = re.sub(pan_pattern, "[MASKED_PAN]", raw_query, flags=re.IGNORECASE)
    sanitized = re.sub(aadhaar_pattern, "[MASKED_AADHAAR]", sanitized)
    sanitized = re.sub(bank_account_pattern, "[MASKED_BANK_ACCOUNT]", sanitized)
    
    return {"sanitized_query": sanitized}

# --- Node 2: Deterministic Router Classification Node ---
def router_node(state: CredAgentState) -> Dict[str, Any]:
    log.info(f"--- Entering Node: [{router_node.__name__}] ---")
    log.info("---  Intent Routing Logic Analyzer ---")
    q = state["sanitized_query"].lower()
    
    policy_keywords = [
            "eligibility", "fee", "kyc", "fraud", "interest", "emi", 
            "closure", "penalty", "slab", "balance", "score", "joint", "nri"
    ]
    
    if any(w in q for w in policy_keywords):
        intent = "policy_rag"
    
    elif "lnk-" in q or any(w in q for w in ["status", "track", "check"]):
        intent = "status_check"
    
    else:
        intent = "out_of_scope"
        
    return {"intent": intent}

# --- Node 3: Policy Vector Database Retrieval Node ---
def rag_node(state: CredAgentState) -> Dict[str, Any]:
    log.info(f"--- Entering Node: [{rag_node.__name__}] ---")
    log.info("---  RAG Policy Store Knowledge Base Retrieval ---")
    # NOTE: Your local vector-database collection query hooks will interface directly here.
    # Defaulting to an operational placeholder string until collection orchestration initializes.
    return {"retrieved_context": "Verified internal policy document context matches."}

# --- Node 4: CSV Data Registry Core Lookup Tool ---
def lookup_node(state: CredAgentState) -> Dict[str, Any]:
    log.info(f"--- Entering Node: [{lookup_node.__name__}] ---")
    log.info("---  CSV Application Data Registry Lookup ---")
    
    user_text = state["sanitized_query"]
    match = re.search(r'LNK-\d+', user_text, re.IGNORECASE)
    if not match:
        log.warning("Lookup failure: Missing valid transaction tracking token reference.")
        return {
            "application_data": {
                "error": "Missing application tracking token. Please provide a reference number structured as LNK-XXXX."
            }
        }
        
    target_id = match.group(0).upper()
    log.info(f"Target Record ID identified: {target_id}")
    
    csv_path = "dataset_persist.csv"
    if not os.path.exists(csv_path):
        log.error(f"Critical error: Primary datastore source '{csv_path}' cannot be verified on disk.")
        return {"application_data": {"error": "Internal ledger storage configuration reference error."}}
        
    matched_row = None
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["record_id"].strip().upper() == target_id:
                matched_row = row
                break 
                
    if not matched_row:
        log.error(f"Operational mismatch: Application identifier {target_id} does not exist in master records.")
        return {"application_data": {"error": f"Application record {target_id} was not found in our systems."}}
        
    log.info(f"Success: Retrieved record matching tracking code {target_id}")
    
    # Task 6 Justification Matrix Calculation Layer
    is_fraud = matched_row["flagged_for_fraud_review"].lower() == "true"
    days = int(matched_row["days_since_created"])
    
    # Escalation Balance Formula Profile: (Fraud * 0.70) + ((Days / 30) * 0.30)
    fraud_weight = 0.70 if is_fraud else 0.0
    recency_weight = (days / 30.0) * 0.30
    escalation_score = round(fraud_weight + recency_weight, 2)
    
    action_recommended = "IMMEDIATE_ESCALATION" if escalation_score >= 0.75 else "STANDARD_QUEUE"
  
    return {
        "application_data": {
            "record_id": matched_row["record_id"],
            "category": matched_row["category"],
            "status": matched_row["status"],
            "loan_amount_inr": int(matched_row["loan_amount_inr"]),
            "escalation_score": escalation_score,
            "action_recommended": action_recommended
        }
    }

# --- Node 5: Deterministic MOCK_LLM Generation Response Compiler Node ---
def generator_node(state: CredAgentState) -> Dict[str, Any]:
    log.info(f"--- Entering Node: [{generator_node.__name__}] ---")
     
    log.info("---  Final Response Generation via Deterministic MOCK_LLM Layer ---")
    
    intent = state.get("intent", "out_of_scope")
    response_string = ""
    escalation_status = "STANDARD_QUEUE"
    
    # Route Execution A: Data parsing from the CSV lookup dataset registry
    if intent == "status_check" and state.get("application_data"):
        data = state["application_data"]
        if "error" in data:
            response_string = f"Account Tracking Exception: {data['error']}"
        else:
            response_string = (
                f"Your loan application request ({data['record_id']}) under category '{data['category']}' "
                f"is currently tracking as '{data['status']}'. Internal verification parameters output a risk profile score "
                f"of {data['escalation_score']}."
            )
            escalation_status = data.get("action_recommended", "STANDARD_QUEUE")
            
    # Route Execution B: Text extraction mapping from the vector storage RAG system
    elif intent == "policy_rag":
        context = state.get("retrieved_context", "")
        if "SORRY" in context or not context:
            response_string = "I am sorry, but the internal verified policy guidelines do not contain enough validated parameters to answer this request."
        else:
            response_string = f"According to verified corporate policies: {context}"
            
    # Route Execution C: Standard fallback for completely out-of-scope traffic queries
    else:
        response_string = "I am only authorized to resolve validated loan policy regulations and active application status tracking inquiries."

    # Validate compiling parameters securely against the strict structured output object template
    payload = {
        "is_safe": True,
        "resolved_intent": intent,
        "response_text": response_string,
        "action_recommended": escalation_status
    }
    
    validated_output = CredAgentResponse(**payload).model_dump()
    return {"final_output": validated_output}

# --- State Machine Graph Build Architecture Configuration ---
log.info("**"*40)
log.info("###### processing begins #######")
workflow = StateGraph(CredAgentState)

workflow.add_node("guardrail", guardrail_node)
workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("lookup", lookup_node)
workflow.add_node("generator", generator_node)

workflow.set_entry_point("guardrail")
workflow.add_edge("guardrail", "router")

def route_decision(state: CredAgentState) -> str:
    if state["intent"] == "status_check":
        return "lookup"
    elif state["intent"] == "policy_rag":
        return "rag"
    else:
        return "end"

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "lookup": "lookup",
        "rag": "rag",
        "end": "generator" 
    }
)

workflow.add_edge("rag", "generator")
workflow.add_edge("lookup", "generator")
workflow.add_edge("generator", END)

#agent_graph = workflow.compile()


# --- Task 15: SQLite Resilience Memory Layer Wrapped inside an explicit compiler function ---
def compile_workflow():
    """
    Establishes persistent storage bounds using SQLite checkpointers 
    and returns a fully compiled state machine instance.
    """
    # 1. Ensure the persistent data output directory exists safely
    os.makedirs("data", exist_ok=True)
    
    # 2. Establish a background persistent storage connection to the local database file
    sqlite_connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
    memory_checkpointer = SqliteSaver(sqlite_connection)
    
    # 3. Log the system setup message safely inside the function boundary context
    log.info("System Notification: Core LangGraph Engine successfully compiled with SQLite Checkpointer Storage Base.")
    
    # 4. Return the fully initialized state graph workflow instance
    return workflow.compile(checkpointer=memory_checkpointer)

# --- GLOBAL ASSIGNMENT (For outward module compatibility) ---
# Call the function once at load-time to expose 'agent_graph' to your server and evaluation sheets
agent_graph = compile_workflow()
