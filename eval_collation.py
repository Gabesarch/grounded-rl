import json
from pathlib import Path

folder = Path("/PATH/TO/EVALUATION/JSON/FOLDER")

total = 0
total_all = 0
for f in folder.glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            data = json.loads(line)
            total_all += 1
            if data.get("judge_score") == 1.0:
                total += 1

print(f"Total judge_score == 1.0: {total} out of {total_all}")

