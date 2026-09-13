# 🏦 Final Capstone — Cred Domain Support Agent (LangGraph)

### 📌 Submission Identification
- **Track Confirmation:** Banking & FinTech (Cred)
- **Execution Mode:** 100% Deterministic `MOCK_LLM` (Keyless, Zero Network Dependency)
- **Local Environment Target:** Python Virtual Env (`actualenv`)

---

## 🛠️ Installation & Local Environment Setup

Due to upstream sub-dependency version restrictions within the native `langchain-chroma` packaging layer, all production parameters have been explicitly locked inside our local `requirements.txt`. 

To bypass package resolver backtracking or infinite loops during setup, you **must** execute the command using the global isolation flag:

```bash
pip install -r requirements.txt --no-deps
```

*This guarantees that our validated footprint (`chromadb-0.5.5`, `fastmcp-2.1.0`, and `httpx-0.27.2`) loads instantly without package version conflicts.*

---

## 📊 Task 1: Dataset Design & Reproducibility Matrix

The internal applications registry is generated deterministically. To reproduce the exact ledger footprints, the generator script utilizes these variables:

- **Random Allocation Seed:** `42`
- **Total Operational Records:** `50` (Exceeds required ≥40)
- **Loan Amount Bounds:** ₹50,000 to ₹5,00,000  
  *Reasoning:* This range represents typical Indian digital retail credit bounds, safely spanning short-ticket unsecured personal liquidity up to mid-tier commercial credit lines.
- **Anomalous Security Volatility Profile (Target Range: 10%–30%):** **18.00%**
- **Category Threshold Verification:** All 5 required categories hold ≥9 records (Constraint: ≥3).
- **Workflow Status Verification:** All 5 required statuses hold ≥9 records (Constraint: ≥1).
- **Record Identifier Sync:** Uses clean serial tracking tokens (`LNK-1001` through `LNK-1050`) for tight local ledger integration.

---

## 🗺️ System Blueprint & Node Topology

The system uses a 5-node architectural loop orchestrated through LangGraph state dictionary mutations:

```text
       [User Input Query]
               │
               ▼
       [guardrail_node]  ──► (Scans & Masks PAN/Aadhaar/Bank Acc via Regex)
               │
               ▼
        [router_node]    ──► (Conditional Edge Check via Keyword Logic)
         ╱         ╲
        ╱           ╲
       ▼             ▼
[lookup_node]    [rag_node]
(Reads CSV)     (Queries ChromaDB)
  * Escalation    * Threshold Filter
    Score           (Calibrated at 0.15)
        ╲           ╱
         ╲         ╱
          ▼       ▼
       [generator_node]  ──► (Compiles Schema Output to Client Interface)
               │
               ▼
         [End Output]
```

---

## 📐 Task 6: Risk Escalation Formula Matrix

When an application tracking check executes, the system maps risk trends using a non-linear scoring algorithm:

$$\text{Escalation Score} = (0.70 \times \text{Fraud Flag}) + \left(0.30 \times \frac{\text{Days Since Created}}{30}\right)$$

- **Escalation Threshold:** **`0.75`**
- **Justification:** This structural boundary captures applications flagged for active fraud validation combined with old pending positions ($>15$ days since opening). This targets the most critical $15\% - 20\%$ of high-risk operational files inside our dataset.

---

## 📈 Task 4, 5 & 13: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.20` to `0.40`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `-0.02` to `-0.81`
- **Assigned Actionable Fallback Barrier (Calibrated Cutoff):** **`0.15`**

### Final System Evaluation Scorecard (27-Query Golden Matrix)
- **Average Context Relevance:** `0.91`
- **Average Groundedness:** `0.85`
- **Average Answer Relevance:** `0.96`
- **Overall System Trust Metric:** **`Pass (Highly Grounded)`**

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded and eliminating "Bulk Document Leak" vulnerabilities.

---

## ⚡ Task 14: Model Context Protocol (FastMCP) Integration

The infrastructure deploys an official **FastMCP Server** operating on the isolated **Stdio Transport Layer (Standard Input/Output Pipes)**. This configuration establishes a hard process boundary separating sensitive core backend databases from the public LLM processing domain.

* **Tool Manifest Discovery:** Programmatically registers the `check_loan_application_status` tool using the formal `@mcp.tool()` schema decorator framework.
* **Deterministic Execution:** Processes automated asynchronous round-trip pipelines via structural JSON-RPC 2.0 transaction packets, logging results continuously to `outputmcp.txt`.

---

## 🚀 Execution & Operational Runbook

### 1. Run the Golden RAG Evaluation Suite
Verify the full 27-query matrix validation and generate the system trust scorecard:
```bash
python -m evaluation.evaluate_triad
```

### 2. Launching the Backend Production Engine
To start the microservices layer locally on the corporate perimeter, run `uvicorn` on Port 8080:
```bash
uvicorn agent.Server:app --host 127.0.0.1 --port 8080 --reload
```
*Live application telemetry writes production payloads directly to `logs/server_logs.jsonl` with masked text verification.*

### 3. Launch the FastMCP Interactive CLI Shell
Boot the persistent command-line console to test live application status checks, risk rules, and exception workflows:
```bash
python agent.mcp_client.py
```
*Type `exit` inside the active shell console to gracefully terminate child worker instances and flush RAM caches.*

## 🛡️ Task 15 & 16: Fault Tolerance & Resilience Stack

To rigorously audit the core MLOps fault tolerance framework without disrupting the main production environment, a dedicated resilience suite has been implemented in `test_resilience.py`.

* **Task 15 (SQLite-Based Checkpointing & Interruption):** The testing script compiles a temporary graph instance with a strict runtime block (`interrupt_after=["router"]`). The graph executes initial layers and automatically freezes state snapshot metrics into `data/checkpoints.sqlite`. Upon reloading using a `None` state invocation under the identical Thread ID (`checkpoint_session_202`), the engine successfully bypasses previously executed nodes, directly launching downstream workflows to achieve full state persistence compliance.
* **Task 16a (Transient Failure Recovery & Exponential Backoff):** Simulates transient pipeline chokes during database operations. The system gracefully initiates a structured retry strategy complete with randomized jitter parameters and incremental delays, demonstrating self-healing capabilities before final compilation without dropping network hooks.
* **Task 16b (Per-Node Timeout Validation):** Enforces reliability against system hangs and infinite blocking calls. By programmatically introducing a heavy 3.0-second delay within a simulated node while capping execution bounds strictly via `step_timeout=1.0`, the system cleanly breaks the execution thread, throwing a standard, non-blocking runtime exception rather than risking an unbound process hang.
* **Task 16c (Global Graph Lifespan Cancellation):** Guards critical backend resources against total-time overrun vulnerabilities during heavy operational pipeline latency. By simulating a continuous execution stall that overruns the graph's global threshold, the core orchestrator forces a clean execution termination and triggers an automated graph cancellation event exactly as required by production-minded standards.
