import os
from langchain_chroma import Chroma
# Note: Hum local function handling ke liye langchain_chroma ka standard loader use kar rahe hain
import logging

logger = logging.getLogger("loggingCentral")

# Projects Paths Base Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_db")

def retrieve_policy_context(query: str) -> str:
    """Queries the local ChromaDB vector store using the exact same local embedding fallback parameters."""
    logger.info(f"RAG Core: Querying local bank policy repository for: {query}")
    
    # Secure validation check if directory exists
    if not os.path.exists(CHROMA_DIR):
        logger.error(f"Critical Matrix Missing: Chroma database directory not found at {CHROMA_DIR}")
        return "Error: Internal Bank Policy Database is offline."

    try:
        # Load Chroma collection (Passing embedding=None enforces the exact same all-MiniLM-L6-v2 local model)
        vector_store = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=None, # Pure mirror reflection mapping matching indexer.py!
            collection_name="hfdc_internal_policies"
        )
        
        # Pull top 2 most mathematically closest matches
        docs = vector_store.similarity_search(query, k=2)
        
        if not docs:
            logger.warning("Vector search returned zero matches for customer query.")
            return "No matching official compliance protocol found for this specific query."

        # Compile matching chunks along with their ultra-rich metadata metrics for LLM evaluation
        formatted_context = ""
        for doc in docs:
            meta = doc.metadata
            formatted_context += (
                f"\n[DOCUMENT MATRIX ACTIVATED]\n"
                f"- Source File Name: {meta.get('source_file')}\n"
                f"- Operational Category: {meta.get('policy_category')}\n"
                f"- Regulatory Body Desk: {meta.get('regulatory_body')}\n"
                f"- Policy Baseline Status: Verified Active Version ({meta.get('last_updated')})\n"
                f"Content Log Details:\n{doc.page_content}\n"
                f"----------------------------------------\n"
            )
            
        logger.info("RAG Core: Successfully formulated contextual knowledge payload blocks.")
        return formatted_context

    except Exception as e:
        logger.error(f"Critical failure inside retrieval execution pipeline: {str(e)}")
        return f"System Matrix Failure parsing vector store elements: {str(e)}"
