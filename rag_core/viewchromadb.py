# --- SYSTEM INTEGRITY NUMPY 2.X COMPATIBILITY LAYER ---
import numpy as np
if not hasattr(np, "float_"):
    np.float_ = np.float64


import os
import chromadb
from loggingCentral import logger as log

# Paths matrix calculation
#base_dir = os.path.dirname(os.path.abspath(__file__))
#chroma_dir = os.path.join(base_dir, "knowledge_base", "chroma_db")

# 1. Project root main directory absolute folder target kijiye
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chroma_dir = os.path.join(base_dir, "knowledge_base", "chroma_db")



log.info(f"Connecting to persistent database perimeter: {chroma_dir}")
client = chromadb.PersistentClient(path=chroma_dir)

# Check all available collection tags safely
collections = client.list_collections()
log.info(f"Available collection names: {[c.name for c in collections]}")

if collections:
    # Mount the exact target policies store index
    collection = client.get_collection(name="cred_internal_policies")
    data = collection.get(limit=35, include=["documents", "metadatas"])
    
    print("\n" + "="*60 + "\n=== CHROMA DB PERSISTED CHUNKS DATA MATRIX ===\n" + "="*60)
    for doc, meta in zip(data["documents"], data["metadatas"]):
        print(f"[Chunk ID]: {meta.get('chunk_id')}")
        print(f"[Source File]: {meta.get('source_file')}")
        print(f"[Text Content Fragment]: {doc[:150]}...")
        print("-"*60)
else:
    log.error("Ledger storage is completely empty. Please run indexer.py first!")
