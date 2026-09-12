import sys
import json
import os
import csv

def lookup_loan_status(record_id: str) -> dict:
    csv_path = "dataset_persist.csv"
    if not os.path.exists(csv_path):
        return {"error": "Database file dataset_persist.csv missing from root."}
        
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["record_id"].strip().upper() == record_id.strip().upper():
                is_fraud = row["flagged_for_fraud_review"].lower() == "true"
                days = int(row["days_since_created"])
                score = round((0.70 if is_fraud else 0.0) + ((days / 30.0) * 0.30), 2)
                return {
                    "record_id": row["record_id"],
                    "category": row["category"],
                    "status": row["status"],
                    "loan_amount_inr": int(row["loan_amount_inr"]),
                    "escalation_score": score,
                    "action_recommended": "IMMEDIATE_ESCALATION" if score >= 0.75 else "STANDARD_QUEUE"
                }
    return {"error": f"Record {record_id} not registered in infrastructure logs."}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line.strip())
            if request.get("method") == "tools/call":
                params = request.get("params", {})
                args = params.get("arguments", {})
                target_id = args.get("record_id", "")
                
                result = lookup_loan_status(target_id)
                
                response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request.get("id", 1)
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": 1}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
