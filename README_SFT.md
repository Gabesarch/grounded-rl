# ViGoRL: Visually Grounded SFT experiments

## Installation

### Clone Repository

```bash
git clone https://github.com/adisahdev/grounded-rl.git
cd grounded-rl
```

### Environment Setup (No flash attention)

```bash
conda create -n grounded-rl python=3.10
conda activate grounded-rl
pip install uv
uv pip install -e .
uv pip install deepspeed==0.16.9

# SFT dependencies
cd src/trainer/offline
uv pip install -e ".[torch,metrics]"
```

---

## Data Setup

Set the dataset path environment variable before running scripts:

```bash
export DATA_ROOT="/data"
```

### Downloading Datasets

Run the provided script to download and extract data:

```bash
python download_data.py
```

Datasets include:

* Spatial reasoning tasks (SAT-2, BLINK)
* Visual search tasks (V\*Bench)
* Web grounding and action tasks (OS-ATLAS, ScreenSpot, VisualWebArena)

## Training Pipeline

### Instruction Training Dataset preparation
For all experiments, set "osatlas_val_MCTS_linearized_chains" in `src/trainer/offline/data/dataset_info.json` to "spatial_reasoning/MCTS_72b_reasoning_chains_val.json". 

### Data Mix 1: Reproducing Baseline
set "osatlas_train_MCTS_linearized_chains" in `src/trainer/offline/data/dataset_info.json` to "spatial_reasoning/MCTS_72b_reasoning_chains_train.json". 

### Data Mix 2: Grounding + visual search Baseline (33%)
```bash
python prepare_jsons.py --task search --fraction 0.33
```

set "osatlas_train_MCTS_linearized_chains" in `src/trainer/offline/data/dataset_info.json` to "spatial_reasoning/spatial_search_merged_0p33.json". 

### Data Mix 3: Grounding + visual search Baseline (66%)
```bash
python prepare_jsons.py --task search --fraction 0.66
```

set "osatlas_train_MCTS_linearized_chains" in `src/trainer/offline/data/dataset_info.json` to "spatial_reasoning/spatial_search_merged_0p66.json". 

### Data Mix 4: Grounding + visual search Baseline (33%)
```bash
python prepare_jsons.py --task web_grounding --fraction 0.33
```

set "osatlas_train_MCTS_linearized_chains" in `src/trainer/offline/data/dataset_info.json` to "spatial_reasoning/spatial_web_grounding_merged_0p33.json". 

### Supervised Fine-Tuning (SFT)

For the four SFT runs reported, the corresponding reasoning chains described above have to be added to `src/trainer/offline/data/dataset_info.json` and the command below run to get corresponding trained models and checkpoints. Set SAVE_STEPS_DEFAULT=200 and export WANDB_API_KEY="" in "examples/train_qwen2_5_vl_sft.sh" to save training logs.

```bash
cd src/trainer/offline
bash examples/train_qwen2_5_vl_sft.sh
```

## Evaluation

* Spatial reasoning (BLINK, SAT-2):

```bash
bash scripts/evaluation/eval_spatial.sh
```

Set eval_type="sat2_test" or "blink" , change MODEL="" to the checkpoints saved in "/data/checkpoints/sft" and change MODEL_TAG="" on the basis of configuration. 

The results from evaluation would be saved in /data/rollouts.

* Collating results

Collect the summary of evaluation for both SAT and BLINK after setting folder = Path("/PATH/TO/EVALUATION/JSON/FOLDER") from /data/rollouts in eval_collation.py:

```bash
python eval_collation.py
```

Only for BLINK, a detailed category wise break an be obtained: 
```bash
python eval_collation.py
```