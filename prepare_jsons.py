import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--task", choices=["search", "web_grounding"], required=True)
parser.add_argument("--fraction", type=float, required=True, help="Fraction of task data to merge (0.0 to 1.0)")
args = parser.parse_args()

with open("data/spatial_reasoning/MCTS_72b_reasoning_chains_train.json") as f:
    data_spatial = json.load(f)

if args.task == "search":
    task_path = "data/visual_search/MCTS_72b_reasoning_chains_train_SINGLETURN.json"
elif args.task == "web_grounding":
    task_path = "data/web_grounding/MCTS_72b_reasoning_chains_train.json"

with open(task_path) as f:
    data_task = json.load(f)

n = int(len(data_task) * args.fraction)
merged = data_spatial + data_task[:n]

fraction_str = f"{args.fraction:.2f}".replace(".", "p")  # e.g. 0.50 -> "0p50"
out_path = f"data/spatial_reasoning/spatial_{args.task}_merged_{fraction_str}.json"

with open(out_path, "w") as f:
    json.dump(merged, f, indent=2)

print(f"Merged {len(data_spatial)} spatial + {n} {args.task} samples -> {out_path}")