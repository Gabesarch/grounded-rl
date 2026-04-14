import json
from pathlib import Path
from collections import defaultdict

folder = Path("/PATH/TO/EVALUATION/JSON/FOLDER")

total = 0
total_all = 0
category_correct = defaultdict(int)
category_total = defaultdict(int)

for f in folder.glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            data = json.loads(line)
            total_all += 1

            # Extract category from id like "val_Art_Style_7" -> "Art_Style"
            raw_id = data.get("id", "")
            parts = raw_id.split("_")
            # Remove first part (e.g. "val") and last part (e.g. "7")
            category = "_".join(parts[1:-1]) if len(parts) > 2 else raw_id

            category_total[category] += 1

            if data.get("judge_score") == 1.0:
                total += 1
                category_correct[category] += 1

print(f"Total judge_score == 1.0: {total} out of {total_all}\n")
print(f"{'Category':<40} {'Correct':>8} {'Total':>8} {'Accuracy':>10}")
print("-" * 70)
for category in sorted(category_total.keys()):
    correct = category_correct[category]
    tot = category_total[category]
    acc = correct / tot * 100 if tot > 0 else 0
    print(f"{category:<40} {correct:>8} {tot:>8} {acc:>9.1f}%")