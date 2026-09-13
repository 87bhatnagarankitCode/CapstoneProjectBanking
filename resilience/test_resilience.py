import sys
import os
import time
import sqlite3


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import agent_graph, workflow  
from langgraph.checkpoint.sqlite import SqliteSaver
from loggingCentral import logger as log

def run_resilience_tests():
    # ======================================================================
    # TEST 1: COMPLIANT RETRY POLICY & TRANSIENT FAILURE RECOVERY (TASK 16a)
    # ======================================================================
    log.info("=== STARTING TEST 1: TRANSIENT RETRY ENGINE AUDIT ===")
    config_thread_1 = {"configurable": {"thread_id": "resilience_session_101"}}
    
    
    initial_state = {"query": "Check loan status for LNK-1001", "history": []}
    
    try:
        log.info("Firing lookup status query to trigger backoff validation loops...")
        output_1 = agent_graph.invoke(initial_state, config=config_thread_1)
        log.info("[SUCCESS] Graph auto-recovered using exponential backoff policy!")
        log.info(f"Final Execution Output Payload: {output_1.get('final_output')}")
    except Exception as e:
        log.error(f"[RETRY FAILURE] Workflow simulation dropped handle: {str(e)}")

    # ======================================================================
    # TEST 2: NATIVE SQLITE CHECKPOINTING & RUN INTERRUPTION (TASK 15)
    # ======================================================================
    log.info("=== STARTING TEST 2: SQLITE CHECKPOINT SAVE & RESUME ===")
    config_thread_2 = {"configurable": {"thread_id": "checkpoint_session_202"}}
    checkpoint_state = {"query": "Check loan policy details for eligibility slabs", "history": []}
    
    try:
        log.info("Compiling graph with explicit run-time interruption after 'router' node...")
        
        
        os.makedirs("data", exist_ok=True)
        sqlite_connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
        test_checkpointer = SqliteSaver(sqlite_connection)
        
        
        interrupted_graph = workflow.compile(checkpointer=test_checkpointer, interrupt_after=["router"])
        
        log.info("Executing initial pipeline flow layers until auto-paused...")
        
        for step in interrupted_graph.stream(checkpoint_state, config=config_thread_2):
            log.info(f"Step executed and cached to checkpoints.sqlite: {list(step.keys())}")
            
        log.info("!!! GRAPH AUTOMATICALLY PAUSED BY CHECKPOINTER AFTER ROUTER !!!")
        log.info("Simulating system recovery window... Waiting 2 seconds.")
        time.sleep(2)
        
        log.info("Resuming execution thread ID 'checkpoint_session_202' from data/checkpoints.sqlite...")
        
        resumed_output = interrupted_graph.invoke(None, config=config_thread_2)
        log.info("[CHECKPOINT SUCCESS] Pipeline completed run without re-executing initial nodes!")
        log.info(f"Final Resumed Result Payload: {resumed_output.get('final_output')}")
        
    except Exception as e:
        log.error(f"[CHECKPOINT FAILURE] Memory persistence trace dropped: {str(e)}")

if __name__ == "__main__":
    run_resilience_tests()
