# --- SYSTEM INTEGRITY NUMPY 2.X COMPATIBILITY LAYER ---
import numpy as np
if not hasattr(np, "float_"):
    np.float_ = np.float64

import os
import re
import csv
import sqlite3
import httpx
import time
import chromadb
from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from loggingCentral import logger as log

class CredAgentResponse(BaseModel):
    is_safe: bool = Field(description="Guardrail bypass indicator status.")
    resolved_intent: str = Field(description="The evaluated query intent routing tag.")
    response_text: str = Field(description="The final textual response generated for member presentation.")
    action_recommended: str = Field(description="Internal operational handling protocol route designation.")

class CredAgentState(TypedDict):
    query: str
    sanitized_query: str
    intent: str
    retrieved_context: str
    application_data: Optional[Dict[str, Any]]
    final_output: Dict[str, Any]
    history: List[Dict[str, str]]
    error: str


def _fetch_from_mcp_server(target_id: str) -> Optional[Dict[str, Any]]:
    """Network-based FastMCP tool lookup bridge."""
    try:
        response = httpx.post(
            "http://127.0.0", # Production standardized standard endpoint path mapping
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "check_loan_application_status", "arguments": {"record_id": target_id}},
                "id": 1
            }, 
            timeout=0.5
        )
        if response.status_code == 200:
            payload = response.json()
            if "result" in payload and "error" not in payload["result"]:
                return payload["result"]
    except Exception:
        pass  
    return None

def _fetch_from_local_ledger(target_id: str) -> Dict[str, Any]:
    """Fallback engine reading from local database storage directly."""
    csv_path = "dataset_persist.csv"
    if not os.path.exists(csv_path):
        return {"error": "Internal database file ledger missing reference context."}
        
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["record_id"].strip().upper() == target_id:
                is_fraud = row["flagged_for_fraud_review"].lower() == "true"
                days = int(row["days_since_created"])
                score = round((0.70 if is_fraud else 0.0) + ((days / 30.0) * 0.30), 2)
                return {
                    "record_id": row["record_id"],
                    "category": row["category"],
                    "status": row["status"],
                    "loan_amount_inr": int(row["loan_amount_inr"]),
                    "escalation_score": score,
                    "action_recommended": "IMMEDIATE_ESCALATION" if score >= 0.75 else "STANDARD_QUEUE"
                }
    return {"error": f"Record {target_id} not registered in infrastructure logs."}


def guardrail_node(state: CredAgentState) -> Dict[str, Any]:
    log.info("--- Entering Node: [guardrail_node] ---")
    raw_query = state["query"]
    pan = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    aadhaar = r'\b[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}\b'
    bank = r'\b[0-9]{9,18}\b'
    sanitized = re.sub(pan, "[MASKED_PAN]", raw_query, flags=re.IGNORECASE)
    sanitized = re.sub(aadhaar, "[MASKED_AADHAAR]", sanitized)
    sanitized = re.sub(bank, "[MASKED_BANK_ACCOUNT]", sanitized)
    return {"sanitized_query": sanitized}

def router_node(state: CredAgentState) -> Dict[str, Any]:
    log.info("--- Entering Node: [router_node] ---")
    q = state["sanitized_query"].lower()
    policy_keywords = ["eligibility", "fee", "kyc", "fraud", "interest", "emi", "closure", "penalty", "slab", "balance", "score", "joint", "nri"]
    if any(w in q for w in policy_keywords):
        intent = "policy_rag"
    elif "lnk-" in q or any(w in q for w in ["status", "track", "check"]):
        intent = "status_check"
    else:
        intent = "out_of_scope"
    return {"intent": intent}


def rag_node(state: CredAgentState) -> Dict[str, Any]:
    log.info("--- Entering Node: [rag_node] ---")
    query_text = state.get("sanitized_query", "")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chroma_path = os.path.join(base_dir, "knowledge_base", "chroma_db", "sentence_based")
    
    retrieved_text = "SORRY"
    
    try:
        
        client = chromadb.PersistentClient(path=chroma_path)
        collection = client.get_collection(name="sentence_based_collection")
        
       
        results = collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        if results and results.get("documents") and results["documents"] and results.get("distances"):
           
            raw_distance = results["distances"][0][0] if isinstance(results["distances"][0], list) else results["distances"][0]
            highest_similarity = round(1.0 - float(raw_distance), 4)
            log.info(f"ChromaDB Query Cosine Similarity Score Evaluated: {highest_similarity}")
            
            # Task 4 & Task 10
            if highest_similarity < 0.15:
                log.info(f"Highest Similarity {highest_similarity} below critical threshold (0.15). Triggering fallback.")
                return {"retrieved_context": "SORRY"}
                
            matched_chunks = results["documents"][0] if isinstance(results["documents"][0], list) else results["documents"]
            retrieved_text = " ".join(matched_chunks).strip()
            log.info(f"Success: Retrieved {len(matched_chunks)} discrete chunks from sentence collection.")
            
    except Exception as e:
        log.error(f"Critical failure inside real ChromaDB retriever node: {str(e)}")
        retrieved_text = "SORRY"
        
    return {"retrieved_context": retrieved_text}


def lookup_node(state: CredAgentState) -> Dict[str, Any]:
    log.info("--- Entering Node: [lookup_node] ---")
    match = re.search(r'LNK-\d+', state["sanitized_query"], re.IGNORECASE)
    if not match:
        return {"application_data": {"error": "Missing application tracking token syntax."}}
    target_id = match.group(0).upper()
    app_data = _fetch_from_mcp_server(target_id)
    if app_data is None:
        app_data = _fetch_from_local_ledger(target_id)
    return {"application_data": app_data}

def generator_node(state: CredAgentState) -> Dict[str, Any]:
    log.info("--- Entering Node: [generator_node] ---")
    intent = state.get("intent", "out_of_scope")
    response_string = ""
    escalation_status = "STANDARD_QUEUE"
    
    context = state.get("retrieved_context", "SORRY")
    
    if intent == "status_check" and state.get("application_data"):
        data = state["application_data"]
        if "error" in data:
            response_string = f"Account Exception: {data['error']}"
        else:
            response_string = f"Your application ({data['record_id']}) is currently tracking as '{data['status']}'. Recency and fraud markers output a risk profile index score of {data['escalation_score']}."
            escalation_status = data.get("action_recommended", "STANDARD_QUEUE")
            
    elif intent == "policy_rag" or intent == "out_of_scope":
        if "SORRY" in context or not context or intent == "out_of_scope":
            response_string = "I am sorry, but the internal policy guidelines do not contain enough parameter metrics to answer this request."
        else:
            response_string = f"According to verified corporate policies: {context}"
    else:
        response_string = "I am only authorized to resolve validated loan policy regulations and active status validation inquiry tracking."
        
    payload = {
        "is_safe": True, 
        "resolved_intent": intent, 
        "response_text": response_string, 
        "action_recommended": escalation_status
    }
    
    return {"final_output": CredAgentResponse(**payload).model_dump()}


workflow = StateGraph(CredAgentState)
workflow.add_node("guardrail", guardrail_node)
workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node, metadata={"timeout": 2.0})
workflow.add_node("lookup", lookup_node, retry={"max_attempts": 4, "initial_interval": 0.5, "max_interval": 2.0, "backoff_factor": 2.0, "jitter": True})
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

workflow.add_conditional_edges("router", route_decision, {"lookup": "lookup", "rag": "rag", "end": "generator"})
workflow.add_edge("rag", "generator")
workflow.add_edge("lookup", "generator")
workflow.add_edge("generator", END)

def compile_workflow():
    os.makedirs("data", exist_ok=True)
    sqlite_connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
    memory_checkpointer = SqliteSaver(sqlite_connection)
    compiled_graph = workflow.compile(checkpointer=memory_checkpointer)
    compiled_graph.step_timeout = 5.0 
    return compiled_graph

_compiled_agent_graph = None
def get_agent_graph():
    global _compiled_agent_graph
    if _compiled_agent_graph is None:
        _compiled_agent_graph = compile_workflow()
    return _compiled_agent_graph

agent_graph = get_agent_graph()
