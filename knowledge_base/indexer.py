import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
from loggingCentral import logger as log

load_dotenv()


# Projects Paths Base Matrix
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "knowledge_base", "documents")
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_db")

def build_policy_index():
    log.info("RAG: ChromaDB local policy indexing starting...")
    
    if not os.path.exists(DOCS_DIR):
        log.error(f"Error: Policy Documents directory missing at: {DOCS_DIR}")
        return False
        
    try:
        # 1. Load Markdown Files (.md policies)
        loader = DirectoryLoader(DOCS_DIR, glob="*.md", loader_cls=TextLoader)
        documents = loader.load()
        log.info(f"Successfully loaded {len(documents)} policy files from documents folder.")

        # 2. Split documents into crisp financial chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        
        # 3. Injecting Enterprise-grade Metadata inside Chunks
        for idx, chunk in enumerate(chunks):
            source_path = chunk.metadata.get("source", "")
            file_name = os.path.basename(source_path)
            category = "Retail Banking Guidelines"
            reg_body = "HFDC-Retail-Operations-Committee"
            
            # File name analytics se category decide karna for examiner view
            
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
            log.info(f"before insert Chunks are as follows : \n  ID{idx} #### Data{chunk.page_content[:50]}")   
            # Rich metadata payload patch
            chunk.metadata.update({
                "source_file": file_name,
                "policy_category": category,
                "last_updated": "Compliance-Q3-2026-v1.0",
                "chunk_id": f"hfdc_sys_chunk_{idx:03d}",
                "access_level": "Level-1-Retail-Support-Desk",
                "regulatory_body": reg_body,
                "token_size_approx": approx_words,
                "is_active_policy": True
            })
            
            

        log.info(f"Metadata processing complete. Total {len(chunks)} chunks created.")
        
        # 4. Save into local ChromaClient (Uses standard built-in local embedding automatically!)
        log.info(f"Persisting vector mapping into secure local perimeter: {CHROMA_DIR}")
        
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=None,  # No OpenAI key! Automatically falls back to free local sentence-transformers architecture inside langchain-chroma
            persist_directory=CHROMA_DIR,
            collection_name="hfdc_internal_policies"
        )
        
        log.info(" SUCCESS: Enterprise ChromaDB local cache memory built successfully!")
        chunks_from_db = vector_store.get()
        for idx, meta in enumerate(chunks_from_db['metadatas']):
            log.info(f" Post Insert in Chroma DB \n,'serial no.'{idx}, 'chunkID'{meta['chunk_id']} 'Source'{meta['source_file']}")
        log.info(" SUCCESS: Enterprise ChromaDB local cache memory built successfully!")
           
        return True

    except Exception as e:
        log.error(f"Critical configuration failure inside indexer core: {str(e)}")
        return False

if __name__ == "__main__":
   
    # --- CENTRALIZED LOGGER RUN SIMULATION MATRIX ---
    print("\n" + "="*60)
    print("CHROMADB CHUNKING SIMULATION LAYER (TEST WINDOW)")
    print("="*60)
    print(build_policy_index())
