import os
import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loggingCentral import logger as log

# Projects Paths Base Matrix
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "knowledge_base", "documents")
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_db")

def enrich_chunk_metadata(chunks, strategy_name):
    """मेटाडेटा इंजेक्शन लॉजिक जो इवैल्यूएशन (Task 5) के लिए सोर्स ट्रैक करेगा"""
    chunk_texts = []
    chunk_metadatas = []
    chunk_ids = []
    
    for idx, chunk in enumerate(chunks):
        source_path = chunk.metadata.get("source", "")
        file_name = os.path.basename(source_path)
        
        category = "Retail Banking Guidelines"
        reg_body = "Cred-Retail-Operations-Committee"
        
        if "eligibility" in file_name.lower():
            category = "Credit Risk & Retail Lending Limits"
            reg_body = "RBI-Credit-Control-Desk"
        elif "emi" in file_name.lower():
            category = "Operational Repayment Auditing Compliance"
            reg_body = "RBI-Banking-Ombudsman-Framework"
        elif "fraud" in file_name.lower():
            category = "Risk Management Security Shield"
            reg_body = "PMLA-Internal-Audit-Cell"

        approx_words = len(chunk.page_content.split())
        generated_id = f"cred_{strategy_name}_{idx:03d}"
        
        
        meta_payload = {
            "source_file": file_name,       
            "policy_category": category,
            "chunk_id": generated_id,
            "strategy": strategy_name,
            "token_size_approx": approx_words,
            "regulatory_body": reg_body,
            "is_active_policy": True
        }
        
        chunk_texts.append(chunk.page_content)
        chunk_metadatas.append(meta_payload)
        chunk_ids.append(generated_id)
        
    return chunk_texts, chunk_metadatas, chunk_ids

def build_policy_index():
    log.info("RAG: Dual Collection Indexing System Activated.")
    
    if not os.path.exists(DOCS_DIR):
        log.error(f"Error: Documents directory missing at: {DOCS_DIR}")
        return False
        
    try:
        
        loader = DirectoryLoader(DOCS_DIR, glob="*.md", loader_cls=TextLoader)
        documents = loader.load()
        log.info(f"Successfully loaded {len(documents)} source policy files.")

        # =====================================================================
        # STRATEGY 1: Pure Fixed-Size with Overlap (No Newlines)
        # =====================================================================
        log.info("Indexing Strategy 1: Fixed-Size (Strict Character Cuts)...")
       
        fixed_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200, 
            chunk_overlap=30,
            separators=[" "] 
        )
        fixed_chunks_raw = fixed_splitter.split_documents(documents)
        f_texts, f_metas, f_ids = enrich_chunk_metadata(fixed_chunks_raw, "fixed_size")
        
        
        fixed_client = chromadb.PersistentClient(path=os.path.join(CHROMA_DIR, "fixed_size"))
        fixed_collection = fixed_client.get_or_create_collection(name="fixed_size_collection")
        fixed_collection.add(documents=f_texts, metadatas=f_metas, ids=f_ids)
        log.info(f"Successfully persisted {len(f_texts)} strict fixed chunks.")

        # =====================================================================
        # STRATEGY 2: Crisp Sentence-Based Chunking
        # =====================================================================
        log.info("Indexing Strategy 2: Sentence-Based (Strict Sentence Cuts)...")
        
        sentence_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, 
            chunk_overlap=0,
            separators=["\n\n", ".\n", ". ", "? ", "! "]
        )
        sentence_chunks_raw = sentence_splitter.split_documents(documents)
        s_texts, s_metas, s_ids = enrich_chunk_metadata(sentence_chunks_raw, "sentence_based")
        
        sentence_client = chromadb.PersistentClient(path=os.path.join(CHROMA_DIR, "sentence_based"))
        sentence_collection = sentence_client.get_or_create_collection(name="sentence_based_collection")
        sentence_collection.add(documents=s_texts, metadatas=s_metas, ids=s_ids)
        log.info(f"Successfully persisted {len(s_texts)} sentence chunks.")

        log.info("COMPLIANCE SUCCESS: Dual collections safely written without any text leaks.")
        return True

    except Exception as e:
        log.error(f"Critical failure inside indexer core: {str(e)}")
        return False

if __name__ == "__main__":
    build_policy_index()
