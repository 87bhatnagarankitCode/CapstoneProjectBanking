import os
import json
import chromadb
from agent.graph import agent_graph
from loggingCentral import logger as log

def runRAGtriadEval():
    log.info("=== Initializing Task 13: 27-Query RAG Triad Evaluation Suite ===")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chroma_path = os.path.join(base_dir, "knowledge_base", "chroma_db", "sentence_based")
    queries_json_path = os.path.join(base_dir, "evaluation", "eval_queries.json")
    
    if not os.path.exists(queries_json_path):
        log.error(f"Error: Golden query matrix missing at: {queries_json_path}")
        return

    with open(queries_json_path, "r", encoding="utf-8") as f:
        EVAL_QUERIES = json.load(f)
    
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection(name="sentence_based_collection")
    
    total_context_rel = 0.0
    total_groundedness = 0.0
    total_answer_rel = 0.0
    records_count = len(EVAL_QUERIES)
    table_rows_cache = []
    
    for idx, item in enumerate(EVAL_QUERIES, 1):
        query = item["q"]
        topic = item["topic"].lower()
        
        db_res = collection.query(query_texts=[query], n_results=3)
        
        highest_similarity = 0.0
        has_chunks = False
        
        if db_res and db_res.get("distances") and db_res["distances"]:
            try:
                dist_list = db_res["distances"]
                if isinstance(dist_list, list) and len(dist_list) > 0:
                    sub_list = dist_list[0]
                    if isinstance(sub_list, list) and len(sub_list) > 0:
                        raw_val = sub_list[0]
                    else:
                        raw_val = sub_list
                else:
                    raw_val = dist_list
                
                highest_similarity = round(1.0 - float(raw_val), 4)
            except Exception:
                highest_similarity = 0.0
            
            if db_res.get("documents") and db_res["documents"]:
                has_chunks = True

        config = {"configurable": {"thread_id": f"eval-session-{idx}"}}
        output = agent_graph.invoke({"query": query, "history": []}, config=config)
        
        final_payload = output.get("final_output", {})
        response_text = final_payload.get("response_text", "").lower()
        resolved_intent = final_payload.get("resolved_intent", "out_of_scope")

        is_refused = "sorry" in response_text or "not contain enough" in response_text

        if "out_of_scope" in topic or is_refused:
            context_rel = 1.0
        else:
            context_rel = 1.0 if has_chunks and highest_similarity >= 0.15 else 0.2

        if is_refused:
            groundedness = 1.0 if "out_of_scope" in topic or highest_similarity < 0.15 else 0.0
        else:
            groundedness = 1.0 if highest_similarity >= 0.15 else 0.0

        if is_refused and (highest_similarity < 0.15 or "out_of_scope" in topic or resolved_intent == "out_of_scope"):
            answer_rel = 1.0
        elif resolved_intent == "out_of_scope" and ("out_of_scope" in topic or "general" in topic):
            answer_rel = 1.0
        elif resolved_intent == "policy_rag" and "status" not in topic:
            answer_rel = 1.0 if not is_refused else 0.0
        elif resolved_intent == "status_check" and "status" in topic:
            answer_rel = 1.0 if "tracking as" in response_text or "account exception" in response_text else 0.0
        else:
            answer_rel = 0.0

        total_context_rel += context_rel
        total_groundedness += groundedness
        total_answer_rel += answer_rel
        
       # row_string = f"{idx:<4} | Sim: {highest_similarity:.2f} | Intent: {resolved_intent:<12} | CR: {context_rel:.2f} | GR: {groundedness:.2f} | AR: {answer_rel:.2f}"
        row_string = f"{idx:<4} | Sim: {highest_similarity:<7.2f} | Intent: {resolved_intent:<12} | CR: {context_rel:.2f} | GR: {groundedness:.2f} | AR: {answer_rel:.2f}"
      
        table_rows_cache.append(row_string)
    
    log.info("="*90)
    log.info(f"{'IDX':<4} | {'SIMILARITY':<10} | {'RESOLVED INT':<12} | {'CONTEXT REL':<11} | {'GROUNDED':<8} | {'ANSWER REL':<10}")
    log.info("="*90)
    for row in table_rows_cache:
        log.info(row)
    log.info("="*90)
    
    avg_context = total_context_rel / records_count
    avg_grounded = total_groundedness / records_count
    avg_answer = total_answer_rel / records_count
    
    log.info("📊 === FINAL AGGREGATE SYSTEM METRICS SCORECARD ===")
    log.info(f"Average Context Relevance: {avg_context:.2f}")
    log.info(f"Average Groundedness:      {avg_grounded:.2f}")
    log.info(f"Average Answer Relevance:  {avg_answer:.2f}")
    log.info("===================================================")

if __name__ == "__main__":
    runRAGtriadEval()
