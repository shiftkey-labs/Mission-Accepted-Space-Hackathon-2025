from pathlib import Path

DATA_ROOT = Path("data/all_source")

OUTPUT_DIR = Path("outputs")
CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"
LOG_DIR = OUTPUT_DIR / "logs"

for d in [OUTPUT_DIR, CHECKPOINT_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

SEQ_LEN = 6
RADIUS_KM = 200
BATCH_SIZE = 4
LR = 1e-3
EPOCHS = 30
DEVICE = "cuda"
