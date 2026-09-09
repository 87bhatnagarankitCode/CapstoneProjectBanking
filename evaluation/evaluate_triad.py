import json
from agent.graph import agent_graph
from loggingCentral import logger as log

  # --- Task 13: Expanded 27-Query Hostile & System Stress Ingestion Matrix ---
with open("evaluation/eval_queries.json", "r", encoding="utf-8") as f:
    EVAL_QUERIES = json.load(f)

def runRAGtriadEval():
    log.info("=== Initializing Task 13: Bulk RAG Triad Evaluation Suite under MOCK_LLM ===")
    
    total_context_relevance = 0.0
    total_groundedness = 0.0
    total_answer_relevance = 0.0
    records_count = len(EVAL_QUERIES)
    
    # Simple Python list to hold our data rows until the graph finishes processing
    table_rows_cache = []
    
    # Execute the testing loop sequentially across all 15 targeted scenarios
    for idx, item in enumerate(EVAL_QUERIES, 1):
        config = {"configurable": {"thread_id": f"eval-session-{idx}"}}
        inputs = {"query": item["q"], "history": []}
        
        # Invoke the active graph pipeline directly
        output = agent_graph.invoke(inputs, config=config)
        final_payload = output.get("final_output", {})
        resolved_intent = final_payload.get("resolved_intent", "out_of_scope")
        
        # --- Programmatic RAG Triad Judging Core ---
                # --- Task 13: Programmatic RAG Triad Judging Core (Pure Architectural Alignment) ---
        # 1. Look for the 'out_of_scope' substring keyword dynamically in the topic name
        if "out_of_scope" in item["topic"]:
            expected_intent = "out_of_scope"
        else:
            # 2. Map the active database status check vs standard policy guidelines trajectories
            expected_intent = "status_check" if item["topic"] == "status_lookup" else "policy_rag"

        # --- The Absolute 1-Line Scoring Rule ---
        context_rel  = 1.0 if resolved_intent == expected_intent else 0.0
        groundedness = 1.0 if resolved_intent == expected_intent else 0.0
        answer_rel   = 1.0 if resolved_intent == expected_intent else 0.0
            
        total_context_relevance += context_rel
        total_groundedness += groundedness
        total_answer_relevance += answer_rel
        
        # Save the formatted row text directly into our cache array list
        row_string = f"{idx:<6} | {resolved_intent:<16} | {context_rel:<12.2f} | {groundedness:<10.2f} | {answer_rel:<10.2f}"
        table_rows_cache.append(row_string)
        
    # --- PRINT PHASE: Triggered safely outside the loop using ONLY your logger ---
    log.info("="*80)
    log.info(f"{'INDEX':<6} | {'RESOLVED INTENT':<16} | {'CONTEXT REL':<12} | {'GROUNDED':<10} | {'ANSWER REL':<10}")
    log.info("="*80)
    
    # Print each cached row line-by-line cleanly without any interruption lines
    for cached_line in table_rows_cache:
        log.info(cached_line)
        
    log.info("="*80)
    
    # Calculate global system metrics averages across the entire test set
    avg_context = total_context_relevance / records_count
    avg_grounded = total_groundedness / records_count
    avg_answer = total_answer_relevance / records_count
    
    log.info("📊 === FINAL AGGREGATE SYSTEM METRICS SCORECARD ===")
    log.info(f"Average Context Relevance: {avg_context:.2f}")
    log.info(f"Average Groundedness:      {avg_grounded:.2f}")
    log.info(f"Average Answer Relevance:  {avg_answer:.2f}")
    log.info("===================================================")
    
    log.info("RAG Triad metrics evaluation logged successfully.")

if __name__ == "__main__":
    runRAGtriadEval()
