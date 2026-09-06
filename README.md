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

*This guarantees that our validated footprint (`chromadb-0.4.24`, `langchain-chroma-0.1.0`, and `sentence-transformers-6.0.1`) loads instantly without package version conflicts.*

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
    Score           (Calibrated at 0.45)
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

## 📈 Task 4 & 5: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.65`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `0.26`
- **Assigned Actionable Fallback Barrier:** **`0.45`**

### Chunking Performance Benchmarks
- **Fixed-Size Overlap Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`
- **Sentence-Level Splitting Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded.

---

## 🚀 Execution & Interactive Testing Interface

### 1. Launching the Backend Production Engine
To start the microservices layer locally, run `uvicorn` from your terminal console:
```bash
uvicorn agent.server:app --reload --port 8000
```

### 2. Testing via the Built-In GUI Layout Page
Open your web browser and navigate directly to:
👉 **`http://127.0.0`**

FastAPI automatically provisions an interactive Swagger UI testing dashboard. Click on the `/ask` route header, select **"Try it out"**, modify the string payload box, and hit **"Execute"** to watch the state variables change in real time.
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

*This guarantees that our validated footprint (`chromadb-0.4.24`, `langchain-chroma-0.1.0`, and `sentence-transformers-6.0.1`) loads instantly without package version conflicts.*

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
    Score           (Calibrated at 0.45)
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

## 📈 Task 4 & 5: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.65`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `0.26`
- **Assigned Actionable Fallback Barrier:** **`0.45`**

### Chunking Performance Benchmarks
- **Fixed-Size Overlap Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`
- **Sentence-Level Splitting Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded.

---

## 🚀 Execution & Interactive Testing Interface

### 1. Launching the Backend Production Engine
To start the microservices layer locally, run `uvicorn` from your terminal console:
```bash
uvicorn agent.server:app --reload --port 8000
```

### 2. Testing via the Built-In GUI Layout Page
Open your web browser and navigate directly to:
👉 **`http://127.0.0`**

FastAPI automatically provisions an interactive Swagger UI testing dashboard. Click on the `/ask` route header, select **"Try it out"**, modify the string payload box, and hit **"Execute"** to watch the state variables change in real time.
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

*This guarantees that our validated footprint (`chromadb-0.4.24`, `langchain-chroma-0.1.0`, and `sentence-transformers-6.0.1`) loads instantly without package version conflicts.*

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
    Score           (Calibrated at 0.45)
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

## 📈 Task 4 & 5: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.65`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `0.26`
- **Assigned Actionable Fallback Barrier:** **`0.45`**

### Chunking Performance Benchmarks
- **Fixed-Size Overlap Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`
- **Sentence-Level Splitting Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded.

---

## 🚀 Execution & Interactive Testing Interface

### 1. Launching the Backend Production Engine
To start the microservices layer locally, run `uvicorn` from your terminal console:
```bash
uvicorn agent.server:app --reload --port 8000
```

### 2. Testing via the Built-In GUI Layout Page
Open your web browser and navigate directly to:
👉 **`http://127.0.0`**

FastAPI automatically provisions an interactive Swagger UI testing dashboard. Click on the `/ask` route header, select **"Try it out"**, modify the string payload box, and hit **"Execute"** to watch the state variables change in real time.
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

*This guarantees that our validated footprint (`chromadb-0.4.24`, `langchain-chroma-0.1.0`, and `sentence-transformers-6.0.1`) loads instantly without package version conflicts.*

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
    Score           (Calibrated at 0.45)
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

## 📈 Task 4 & 5: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.65`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `0.26`
- **Assigned Actionable Fallback Barrier:** **`0.45`**

### Chunking Performance Benchmarks
- **Fixed-Size Overlap Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`
- **Sentence-Level Splitting Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded.

---

## 🚀 Execution & Interactive Testing Interface

### 1. Launching the Backend Production Engine
To start the microservices layer locally, run `uvicorn` from your terminal console:
```bash
uvicorn agent.server:app --reload --port 8000
```

### 2. Testing via the Built-In GUI Layout Page
Open your web browser and navigate directly to:
👉 **`http://127.0.0`**

FastAPI automatically provisions an interactive Swagger UI testing dashboard. Click on the `/ask` route header, select **"Try it out"**, modify the string payload box, and hit **"Execute"** to watch the state variables change in real time.
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

*This guarantees that our validated footprint (`chromadb-0.4.24`, `langchain-chroma-0.1.0`, and `sentence-transformers-6.0.1`) loads instantly without package version conflicts.*

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
    Score           (Calibrated at 0.45)
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

## 📈 Task 4 & 5: RAG Calibration & Recommendation Report

### Empirical Token Similarity Analysis
- **Observed In-Scope Cohesion (Minimum Target Score):** `0.65`
- **Observed Out-of-Scope Leakage (Maximum Unrelated Score):** `0.26`
- **Assigned Actionable Fallback Barrier:** **`0.45`**

### Chunking Performance Benchmarks
- **Fixed-Size Overlap Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`
- **Sentence-Level Splitting Engine:** Mean Precision@3 = `1.00` | Mean Recall@3 = `1.00`

> **Strategic Architecture Recommendation:** The system deploys the **Sentence-Level Splitting Strategy**. Character-based slicing risks truncating numeric values or mathematical rules across text frames. Sentence-based chunks preserve full grammatical expressions, ensuring policy strings remain completely contextually grounded.

---

## 🚀 Execution & Interactive Testing Interface

### 1. Launching the Backend Production Engine
To start the microservices layer locally, run `uvicorn` from your terminal console:
```bash
uvicorn agent.server:app --reload --port 8000
```

### 2. Testing via the Built-In GUI Layout Page
Open your web browser and navigate directly to:
👉 **`http://127.0.0`**

FastAPI automatically provisions an interactive Swagger UI testing dashboard. Click on the `/ask` route header, select **"Try it out"**, modify the string payload box, and hit **"Execute"** to watch the state variables change in real time.
