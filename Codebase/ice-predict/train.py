import torch
from torch.utils.data import DataLoader, random_split
from torch.optim import Adam
from seaice_forecast.dataset import SeaIceDataset
from seaice_forecast.model_3dcnn import SeaIce3DCNN
from seaice_forecast.train_utils import train_epoch, validate_epoch
from seaice_forecast.config import *

def main():
    dataset = SeaIceDataset(DATA_ROOT, seq_len=SEQ_LEN, radius_km=RADIUS_KM)
    n_total = len(dataset)
    n_train = int(n_total * 0.8)
    n_val = n_total - n_train
    train_ds, val_ds = random_split(dataset, [n_train, n_val])

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    device = torch.device(DEVICE if torch.cuda.is_available() else "cpu")
    model = SeaIce3DCNN(in_seq=SEQ_LEN).to(device)
    opt = Adam(model.parameters(), lr=LR)

    print(f"🧊 Training 3D CNN ({n_total} samples) on {device}")
    for epoch in range(EPOCHS):
        train_loss = train_epoch(model, train_loader, opt, device)
        val_loss = validate_epoch(model, val_loader, device)
        print(f"Epoch {epoch+1:03d} | train={train_loss:.4f} | val={val_loss:.4f}")

        # save every 5 epoch
        if (epoch + 1) % 5 == 0:
            ckpt_path = CHECKPOINT_DIR / f"3dcnn_epoch{epoch+1:03d}.pth"
            torch.save(model.state_dict(), ckpt_path)
            print(f"💾 Saved checkpoint: {ckpt_path}")

    print(f"Training complete. Final model saved in {CHECKPOINT_DIR}")

if __name__ == "__main__":
    main()
