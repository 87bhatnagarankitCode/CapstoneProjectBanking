# HFDC BANK - REPAYMENT COMPLIANCE, BOUNCE PENALTY, AND ASSET CLASSIFICATION POLICY
**Document Ref:** HFDC/OPS/REPAY-2026/V1
**Classification:** Public-Facing Operational Guidelines

## SECTION 1: AMORTIZATION TIMELINES & NACH MANDATES
### 1.1 Settlement Architecture
* All retail lending instruments (Personal, Auto, Home Loans) operate on a fixed monthly cycle. EMIs are programmatically pulled via NACH (National Automated Clearing House) or ECS mandates on the **5th of every calendar month**.
* **Grace Period Immunity:** There is **NO grace period** allocated for interest computation. If the 5th falls on a Sunday or a National Clearing Holiday, the transaction retry is scheduled for the next immediate working day, but interest accrued remains uninterrupted.

## SECTION 2: NON-PAYMENT PENAL ACTIONS & FISCAL DRIFT
### 2.1 Technical & Financial Bounces
* **Flat Penalty Rate:** Any NACH/ECS mandate return triggered by "Insufficient Funds" or "Exceeds Arrangement" will incur a flat systemic penalty of **₹500 + 18% GST (Total ₹590)** per automated presentation failure.
* **Penal Interest Compounding:** Overdue balances are subjected to an additional, non-refundable penal interest rate of **2% per month (24% per annum)** calculated on a daily pro-rata basis from the 6th day of the default month until liquidation.

### 2.2 Credit Bureau (RBI Reporting Compliance)
* **DPD (Days Past Due) Tracking:** DPD tracking begins on the 6th day of the month.
* **CIBIL Degradation Alert:** If a bounced EMI remains unresolved for > 72 hours from the presentation window, a negative report packet is pushed to TransUnion CIBIL, Experian, and CRIF High Mark. This automated compliance push typically results in an immediate structural drop of 15 to 30 points in the consumer's credit score.
* **SMA/NPA Classification:** Delinquent assets are categorized under standard RBI mandates:
  - 1 to 30 DPD: Special Mention Account 0 (SMA-0)
  - 31 to 60 DPD: Special Mention Account 1 (SMA-1)
  - 61 to 90 DPD: Special Mention Account 2 (SMA-2)
  - \> 90 DPD: Non-Performing Asset (NPA) - Handed over to the Legal Asset Recovery Cell under the SARFAESI Act.
