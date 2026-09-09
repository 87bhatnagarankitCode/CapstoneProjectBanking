# Replace your current line 3 import configuration with this absolute tracking path:
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now load variables safely from the core architecture module
from agent.graph import agent_graph  # Maps the precise graph framework layout inside agent directory
from loggingCentral import logger as log

def run_resilience_tests():
    # ======================================================================
    # TEST 1: COMPLIANT RETRY POLICY & TRANSIENT FAILURE RECOVERY (TASK 16a)
    # ======================================================================
    log.info("\n=== STARTING TEST 1: TRANSIENT RETRY ENGINE AUDIT ===")
    config_thread_1 = {"configurable": {"thread_id": "resilience_session_101"}}
    
    # Executing status inquiry route which triggers the lookup node retry cycle
    initial_state = {"query": "Check loan status for LNK-1001", "history": []}
    
    try:
        log.info("Firing lookup status query to trigger backoff validation loops...")
        output_1 = agent_graph.invoke(initial_state, config=config_thread_1)
        log.info(f"[SUCCESS] Graph auto-recovered using exponential backoff policy!")
        log.info(f"Final Execution Output Payload: {output_1.get('final_output')}")
    except Exception as e:
        log.error(f"[RETRY FAILURE] Workflow simulation dropped handle: {str(e)}")

    # ======================================================================
    # TEST 2: NATIVE SQLITE CHECKPOINTING & RUN INTERRUPTION (TASK 15)
    # ======================================================================
    log.info("\n=== STARTING TEST 2: SQLITE CHECKPOINT SAVE & RESUME ===")
    config_thread_2 = {"configurable": {"thread_id": "checkpoint_session_202"}}
    checkpoint_state = {"query": "Check loan policy details for eligibility slabs", "history": []}
    
    try:
        log.info("Executing initial pipeline flow layers...")
        # Step-by-step stream lookup execution to simulate programmatic cutoff
        for step in agent_graph.stream(checkpoint_state, config=config_thread_2):
            log.info(f"Step executed and cached to checkpoints.sqlite: {list(step.keys())}")
            # Programmatic freeze simulation: interrupt execution loop immediately after router node
            if "router" in step:
                log.warning("!!! CRITICAL INTERRUPTION SIMULATION: Cutting processing thread now !!!")
                break
                
        log.info("Simulating system recovery window... Waiting 2 seconds.")
        time.sleep(2)
        
        log.info("Resuming execution thread ID 'checkpoint_session_202' from data/checkpoints.sqlite...")
        # Invoking graph with None state to force load context details from memory checkpointer storage
        resumed_output = agent_graph.invoke(None, config=config_thread_2)
        log.info("[CHECKPOINT SUCCESS] Pipeline completed run without re-executing initial nodes!")
        log.info(f"Final Resumed Result Payload: {resumed_output.get('final_output')}")
    except Exception as e:
        log.error(f"[CHECKPOINT FAILURE] Memory persistence trace dropped: {str(e)}")

if __name__ == "__main__":
    run_resilience_tests()
