"""
SIP Saathi - Golden dataset evaluation (v2)
-------------------------------------------
Run from your project folder (the one that contains app.py):

    python evaluate.py                                       -> tests knowledge/sip_knowledge.json
    python evaluate.py knowledge/sip_knowledge_before.json   -> tests the old version

Results are saved to data/eval_results_<file name>.csv
"""

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
DEFAULT_KB = BASE / "knowledge" / "sip_knowledge.json"

# None = out of scope: the assistant should NOT give an answer
# (no fund recommendations, no predictions, no unrelated topics).
GOLDEN = [
    # ---- Failed SIP payment ----
    ("My SIP payment failed this month", "Failed SIP payment"),
    ("SIP installment failed because of insufficient balance", "Failed SIP payment"),
    ("Money was not debited and my SIP failed", "Failed SIP payment"),
    ("Why did my SIP debit fail?", "Failed SIP payment"),
    ("My SIP debit failed because of low balance", "Failed SIP payment"),

    # ---- AutoPay mandate problem ----
    ("AutoPay mandate got rejected for my SIP", "AutoPay mandate problem"),
    ("My SIP mandate has expired", "AutoPay mandate problem"),
    ("How do I set up AutoPay for my SIP?", "AutoPay mandate problem"),
    ("Bank mandate approval is pending for my SIP", "AutoPay mandate problem"),
    ("My AutoPay is not active", "AutoPay mandate problem"),

    # ---- Missed SIP instalment ----
    ("I missed my SIP instalment this month", "Missed SIP instalment"),
    ("My SIP installment did not go through, what should I do", "Missed SIP instalment"),
    ("SIP was skipped for this month", "Missed SIP instalment"),
    ("I forgot to keep balance and missed a SIP date", "Missed SIP instalment"),
    ("Will a missed SIP instalment have a penalty?", "Missed SIP instalment"),

    # ---- Thinking about pausing ----
    ("I want to pause my SIP for a few months", "Thinking about pausing"),
    ("Can I temporarily stop my SIP?", "Thinking about pausing"),
    ("Money is tight, should I pause my SIP?", "Thinking about pausing"),
    ("How do I pause my SIP in the app?", "Thinking about pausing"),
    ("I am thinking of pausing my SIP because the market is down", "Thinking about pausing"),

    # ---- Understanding SIP ----
    ("What is a SIP?", "Understanding SIP"),
    ("How does a systematic investment plan work?", "Understanding SIP"),
    ("Explain SIP to a beginner", "Understanding SIP"),
    ("How does SIP investing work in mutual funds?", "Understanding SIP"),
    ("What does SIP stand for?", "Understanding SIP"),

    # ---- Cancelling SIP ----
    ("How do I cancel my SIP?", "Cancelling SIP"),
    ("I want to stop my SIP permanently", "Cancelling SIP"),
    ("Steps to cancel SIP in Groww", "Cancelling SIP"),
    ("Can I close my SIP before the next instalment date?", "Cancelling SIP"),
    ("How to discontinue my mutual fund SIP", "Cancelling SIP"),

    # ---- Out of scope / guardrail tests (expected: no answer) ----
    ("Which mutual fund should I buy?", None),
    ("What return will my SIP give next year?", None),
    ("Tell me today's weather in Bhopal", None),
    ("Is the Nifty going to crash tomorrow?", None),
    ("Help me pay my credit card bill", None),
    ("Which is the best stock to buy this week?", None),
]


def load_kb(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_problem(question, kb):
    """Same logic as detect_problem() in app.py."""
    text = question.lower()
    best_match, highest_score = None, 0
    for item in kb:
        score = sum(1 for kw in item["keywords"] if kw.lower() in text)
        if score > highest_score:
            highest_score = score
            best_match = item["topic"]
    return best_match


def main():
    kb_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_KB
    if not kb_path.is_absolute():
        kb_path = Path.cwd() / kb_path
    out_path = BASE / "data" / f"eval_results_{kb_path.stem}.csv"

    kb = load_kb(kb_path)
    topics = [item["topic"] for item in kb]

    print(f"Testing: {kb_path.name}")
    print("Topics found:")
    for t in topics:
        print("  -", t)

    expected_topics = {e for _, e in GOLDEN if e is not None}
    missing = expected_topics - set(topics)
    if missing:
        print("\nNOTE: these topics are tested but missing from this file:")
        for m in sorted(missing):
            print("  -", m)

    rows = []
    per_topic = defaultdict(lambda: [0, 0])

    for question, expected in GOLDEN:
        predicted = detect_problem(question, kb)
        correct = predicted == expected
        label = expected if expected else "OUT OF SCOPE"
        per_topic[label][1] += 1
        per_topic[label][0] += int(correct)
        rows.append({
            "question": question,
            "expected": label,
            "predicted": predicted if predicted else "NO ANSWER",
            "correct": "YES" if correct else "NO",
        })

    total = len(rows)
    correct_total = sum(1 for r in rows if r["correct"] == "YES")
    in_scope = [r for r in rows if r["expected"] != "OUT OF SCOPE"]
    out_scope = [r for r in rows if r["expected"] == "OUT OF SCOPE"]
    in_acc = sum(1 for r in in_scope if r["correct"] == "YES") / len(in_scope)
    out_acc = sum(1 for r in out_scope if r["correct"] == "YES") / len(out_scope)

    print("\n================ RESULTS ================")
    print(f"Overall accuracy:            {correct_total}/{total} = {correct_total/total:.0%}")
    print(f"In-scope topic accuracy:     {in_acc:.0%}")
    print(f"Out-of-scope safely refused: {out_acc:.0%}  (guardrail metric)")
    print("\nPer topic:")
    for label, (c, n) in per_topic.items():
        print(f"  {label:<28} {c}/{n}")

    failures = [r for r in rows if r["correct"] == "NO"]
    if failures:
        print("\nFailed cases:")
        for r in failures:
            print(f"  Q: {r['question']}")
            print(f"     expected: {r['expected']} | got: {r['predicted']}")

    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["question", "expected", "predicted", "correct"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved detailed results to {out_path}")
    print(f"Run date: {datetime.now():%d-%m-%Y %H:%M}")


if __name__ == "__main__":
    main()
