import random, uuid
from collections import Counter
from loggingCentral import logger as log
import csv

SEED = 42
random.seed(SEED)

CATEGORIES = ["Personal Loan", "Home Loan", "Auto Loan", "Education Loan", "Business Loan"]
STATUSES = ["Submitted", "Under Review", "Approved", "Rejected", "Disbursed"]

MIN_AMOUNT = 50_000
MAX_AMOUNT = 5_000_000

def generate_dataset(n=40):
    log.info("######      Generating dataset with %d records      ######", n)
    dataset = []
    for _ in range(n):
        record = {
            "record_id": str(uuid.uuid4().hex[:15]),
            "category": random.choice(CATEGORIES),
            "status": random.choice(STATUSES),
            "loan_amount_inr": random.randint(MIN_AMOUNT, MAX_AMOUNT),
            "days_since_created": random.randint(0, 30),
            "flagged_for_fraud_review": random.random() < 0.2
        }
        dataset.append(record)
    log.info("######      Dataset generation complete      ######")
    return dataset

def validate_dataset(dataset):
    category_counts = Counter([d["category"] for d in dataset])
    status_counts = Counter([d["status"] for d in dataset])
    fraud_percentage = sum(d["flagged_for_fraud_review"] for d in dataset) / len(dataset) * 100

    log.info("=== Validation Report ===")
    log.info(f"Category counts: {category_counts}")
    log.info(f"Status counts: {status_counts}")
    log.info(f"Fraud review percentage: {fraud_percentage:.2f}%")
    log.info("=========================")


def save_dataset_csv(dataset, filename="dataset_persist.csv"):
    if not dataset:
        log.error("Dataset is empty, nothing to save.")
        return
    fieldnames = dataset[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:       
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

    log.info(f"Dataset saved to {filename}")


if __name__ == "__main__":
    dataset = generate_dataset(50)
    validate_dataset(dataset)
    log.debug(f"Sample record: {dataset[0]}")
    save_dataset_csv(dataset)

